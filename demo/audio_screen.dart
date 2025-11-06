import 'dart:io';
import 'package:flutter/material.dart';
import 'package:audio_waveforms/audio_waveforms.dart';
import 'package:path_provider/path_provider.dart';
import 'package:permission_handler/permission_handler.dart';
import 'package:intl/intl.dart';
import 'package:speech_to_text/speech_to_text.dart' as stt;

class AudioRecorderScreen extends StatefulWidget {
  const AudioRecorderScreen({super.key});

  @override
  State<AudioRecorderScreen> createState() => _AudioRecorderScreenState();
}

class _AudioRecorderScreenState extends State<AudioRecorderScreen> {
  late RecorderController _recorderController;
  PlayerController? _playerController;
  late stt.SpeechToText _speechToText;
  
  bool _isRecording = false;
  bool _isPlaying = false;
  bool _permissionGranted = false;
  bool _speechEnabled = false;
  String _statusText = 'Tap microphone to start recording';
  String _transcribedText = '';
  List<Recording> _recordings = [];
  String? _currentPlayingPath;
  
  @override
  void initState() {
    super.initState();
    _recorderController = RecorderController();
    _speechToText = stt.SpeechToText();
    _initializeSpeech();
    _requestPermissions();
    _loadRecordings();
  }
  
  Future<void> _initializeSpeech() async {
    try {
      bool available = await _speechToText.initialize(
        onStatus: (status) => debugPrint('Speech status: $status'),
        onError: (error) => debugPrint('Speech error: $error'),
      );
      setState(() => _speechEnabled = available);
      if (!available) {
        debugPrint('Speech recognition not available');
      }
    } catch (e) {
      debugPrint('Failed to initialize speech recognition: $e');
    }
  }
  
  Future<void> _requestPermissions() async {
    final status = await Permission.microphone.request();
    setState(() {
      _permissionGranted = status.isGranted;
      if (!_permissionGranted) {
        _statusText = 'Microphone permission denied. Tap to request again.';
      } else {
        _statusText = 'Ready! Tap microphone to start recording';
      }
    });
  }
  
  Future<String> _getFilePath() async {
    final directory = await getApplicationDocumentsDirectory();
    final timestamp = DateFormat('yyyyMMdd_HHmmss').format(DateTime.now());
    return '${directory.path}/recording_$timestamp.m4a';
  }
  
  Future<void> _loadRecordings() async {
    try {
      final directory = await getApplicationDocumentsDirectory();
      final files = Directory(directory.path)
          .listSync()
          .where((item) => item.path.endsWith('.m4a'))
          .map((item) => File(item.path))
          .toList();
      
      files.sort((a, b) => b.lastModifiedSync().compareTo(a.lastModifiedSync()));
      
      setState(() {
        _recordings = files
            .map((file) => Recording(
                  path: file.path,
                  name: file.path.split(Platform.pathSeparator).last,
                  date: file.lastModifiedSync(),
                ))
            .toList();
      });
    } catch (e) {
      debugPrint('Error loading recordings: $e');
    }
  }
  
  Future<void> _startRecording() async {
    if (!_permissionGranted) {
      await _requestPermissions();
      if (!_permissionGranted) return;
    }
    
    try {
      final path = await _getFilePath();
      
      // Start audio recording
      await _recorderController.record(path: path);
      
      // Start live speech recognition
      if (_speechEnabled) {
        await _speechToText.listen(
          onResult: (result) {
            setState(() {
              _transcribedText = result.recognizedWords;
              _statusText = '🎤 Recording... "${_transcribedText}"';
            });
          },
          listenMode: stt.ListenMode.dictation,
          partialResults: true,
          cancelOnError: false,
        );
      }
      
      setState(() {
        _isRecording = true;
        if (!_speechEnabled) {
          _statusText = '🎤 Recording... (Speech recognition unavailable)';
        }
      });
      
      debugPrint('Recording started: $path');
    } catch (e) {
      debugPrint('Error starting recording: $e');
      setState(() {
        _statusText = 'Error: $e';
      });
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Recording error: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }
  
  Future<void> _stopRecording() async {
    try {
      final path = await _recorderController.stop();
      
      // Stop speech recognition
      if (_speechEnabled && _speechToText.isListening) {
        await _speechToText.stop();
      }
      
      setState(() {
        _isRecording = false;
        _statusText = 'Recording saved! Tap to record again';
      });
      
      debugPrint('Recording stopped: $path');
      
      await _loadRecordings();
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('✅ Recording saved successfully!'),
            backgroundColor: Colors.green,
            duration: Duration(seconds: 2),
          ),
        );
      }
      
      // Clear transcription after a delay
      Future.delayed(const Duration(seconds: 2), () {
        if (mounted) {
          setState(() => _transcribedText = '');
        }
      });
    } catch (e) {
      debugPrint('Error stopping recording: $e');
      setState(() {
        _statusText = 'Error stopping: $e';
        _transcribedText = '';
      });
    }
  }
  
  Future<void> _toggleRecording() async {
    if (_isRecording) {
      await _stopRecording();
    } else {
      await _startRecording();
    }
  }
  
  Future<void> _playRecording(String path) async {
    try {
      // Stop current playback if any
      if (_isPlaying && _currentPlayingPath != null) {
        await _playerController?.stopPlayer();
        setState(() {
          _isPlaying = false;
          _currentPlayingPath = null;
        });
        
        // If clicking the same file, just stop
        if (_currentPlayingPath == path) {
          return;
        }
      }
      
      // Create new player controller
      _playerController = PlayerController();
      await _playerController!.preparePlayer(
        path: path,
        shouldExtractWaveform: false,
      );
      
      await _playerController!.startPlayer();
      
      setState(() {
        _isPlaying = true;
        _currentPlayingPath = path;
      });
      
      // Listen for completion
      _playerController!.onCompletion.listen((_) {
        if (mounted) {
          setState(() {
            _isPlaying = false;
            _currentPlayingPath = null;
          });
        }
      });
    } catch (e) {
      debugPrint('Error playing recording: $e');
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Playback error: $e'),
            backgroundColor: Colors.red,
          ),
        );
      }
    }
  }
  
  Future<void> _deleteRecording(Recording recording) async {
    try {
      // Stop if currently playing this file
      if (_currentPlayingPath == recording.path) {
        await _playerController?.stopPlayer();
        setState(() {
          _isPlaying = false;
          _currentPlayingPath = null;
        });
      }
      
      final file = File(recording.path);
      await file.delete();
      await _loadRecordings();
      
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Recording deleted'),
            duration: Duration(seconds: 1),
          ),
        );
      }
    } catch (e) {
      debugPrint('Error deleting recording: $e');
    }
  }
  
  @override
  void dispose() {
    _recorderController.dispose();
    _playerController?.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Audio Recorder'),
        backgroundColor: Theme.of(context).colorScheme.inversePrimary,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh),
            onPressed: _loadRecordings,
            tooltip: 'Refresh recordings',
          ),
        ],
      ),
      body: Column(
        children: [
          // Recording Section
          Expanded(
            flex: 2,
            child: Container(
              decoration: BoxDecoration(
                gradient: LinearGradient(
                  begin: Alignment.topCenter,
                  end: Alignment.bottomCenter,
                  colors: [
                    _isRecording ? Colors.red[50]! : Colors.blue[50]!,
                    Colors.white,
                  ],
                ),
              ),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  // Status Text
                  Padding(
                    padding: const EdgeInsets.all(16),
                    child: Text(
                      _statusText,
                      textAlign: TextAlign.center,
                      style: TextStyle(
                        fontSize: 18,
                        fontWeight: FontWeight.bold,
                        color: _isRecording ? Colors.red[900] : Colors.blue[900],
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 20),
                  
                  // Record Button
                  GestureDetector(
                    onTap: _permissionGranted ? _toggleRecording : _requestPermissions,
                    child: Container(
                      width: 120,
                      height: 120,
                      decoration: BoxDecoration(
                        shape: BoxShape.circle,
                        color: _isRecording ? Colors.red : Colors.blue,
                        boxShadow: [
                          BoxShadow(
                            color: _isRecording 
                                ? Colors.red.withOpacity(0.5)
                                : Colors.blue.withOpacity(0.5),
                            blurRadius: 20,
                            spreadRadius: 5,
                          ),
                        ],
                      ),
                      child: Icon(
                        _isRecording ? Icons.stop : Icons.mic,
                        size: 60,
                        color: Colors.white,
                      ),
                    ),
                  ),
                  
                  const SizedBox(height: 20),
                  
                  // Recording indicator
                  if (_isRecording)
                    Container(
                      padding: const EdgeInsets.symmetric(horizontal: 20, vertical: 10),
                      decoration: BoxDecoration(
                        color: Colors.red,
                        borderRadius: BorderRadius.circular(20),
                      ),
                      child: const Row(
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          Icon(Icons.fiber_manual_record, color: Colors.white, size: 16),
                          SizedBox(width: 8),
                          Text(
                            'RECORDING',
                            style: TextStyle(
                              color: Colors.white,
                              fontWeight: FontWeight.bold,
                            ),
                          ),
                        ],
                      ),
                    ),
                  
                  // Transcription Display
                  if (_transcribedText.isNotEmpty)
                    Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 16),
                      child: Container(
                        padding: const EdgeInsets.all(16),
                        constraints: const BoxConstraints(maxHeight: 150),
                        decoration: BoxDecoration(
                          color: Colors.grey[100],
                          borderRadius: BorderRadius.circular(12),
                          border: Border.all(color: Colors.blue[200]!),
                        ),
                        child: SingleChildScrollView(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Row(
                                children: [
                                  Icon(Icons.text_fields, size: 16, color: Colors.blue[700]),
                                  const SizedBox(width: 8),
                                  Text(
                                    'Live Transcription:',
                                    style: TextStyle(
                                      fontSize: 12,
                                      fontWeight: FontWeight.bold,
                                      color: Colors.blue[700],
                                    ),
                                  ),
                                ],
                              ),
                              const SizedBox(height: 8),
                              Text(
                                _transcribedText,
                                style: const TextStyle(
                                  fontSize: 16,
                                  height: 1.4,
                                ),
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                ],
              ),
            ),
          ),
          
          // Divider
          const Divider(height: 1, thickness: 2),
          
          // Recordings List
          Expanded(
            flex: 3,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Padding(
                  padding: const EdgeInsets.all(16),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Text(
                        'Saved Recordings (${_recordings.length})',
                        style: const TextStyle(
                          fontSize: 18,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      if (_recordings.isNotEmpty)
                        Text(
                          '${(_recordings.fold<int>(0, (sum, r) => sum + File(r.path).lengthSync()) / (1024 * 1024)).toStringAsFixed(2)} MB',
                          style: TextStyle(
                            fontSize: 14,
                            color: Colors.grey[600],
                          ),
                        ),
                    ],
                  ),
                ),
                Expanded(
                  child: _recordings.isEmpty
                      ? Center(
                          child: Column(
                            mainAxisAlignment: MainAxisAlignment.center,
                            children: [
                              Icon(
                                Icons.mic_none,
                                size: 64,
                                color: Colors.grey[400],
                              ),
                              const SizedBox(height: 16),
                              Text(
                                'No recordings yet',
                                style: TextStyle(
                                  fontSize: 16,
                                  color: Colors.grey[600],
                                ),
                              ),
                              const SizedBox(height: 8),
                              Text(
                                'Tap the microphone button to start',
                                style: TextStyle(
                                  fontSize: 14,
                                  color: Colors.grey[500],
                                ),
                              ),
                            ],
                          ),
                        )
                      : ListView.builder(
                          itemCount: _recordings.length,
                          itemBuilder: (context, index) {
                            final recording = _recordings[index];
                            final fileSize = File(recording.path).lengthSync();
                            final fileSizeKB = (fileSize / 1024).toStringAsFixed(2);
                            final isCurrentlyPlaying = _isPlaying && _currentPlayingPath == recording.path;
                            
                            return Card(
                              margin: const EdgeInsets.symmetric(
                                horizontal: 16,
                                vertical: 8,
                              ),
                              elevation: isCurrentlyPlaying ? 4 : 1,
                              color: isCurrentlyPlaying ? Colors.green[50] : null,
                              child: ListTile(
                                leading: CircleAvatar(
                                  backgroundColor: isCurrentlyPlaying ? Colors.green : Colors.blue,
                                  child: Icon(
                                    isCurrentlyPlaying ? Icons.volume_up : Icons.audiotrack,
                                    color: Colors.white,
                                  ),
                                ),
                                title: Text(
                                  recording.name,
                                  style: const TextStyle(fontWeight: FontWeight.bold),
                                  overflow: TextOverflow.ellipsis,
                                ),
                                subtitle: Text(
                                  '${DateFormat('MMM d, yyyy HH:mm').format(recording.date)}\n$fileSizeKB KB',
                                ),
                                isThreeLine: true,
                                trailing: Row(
                                  mainAxisSize: MainAxisSize.min,
                                  children: [
                                    IconButton(
                                      icon: Icon(
                                        isCurrentlyPlaying ? Icons.stop : Icons.play_arrow,
                                        color: Colors.green,
                                      ),
                                      onPressed: () => _playRecording(recording.path),
                                    ),
                                    IconButton(
                                      icon: const Icon(Icons.delete, color: Colors.red),
                                      onPressed: () => _deleteRecording(recording),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          },
                        ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class Recording {
  final String path;
  final String name;
  final DateTime date;
  
  Recording({
    required this.path,
    required this.name,
    required this.date,
  });
}
