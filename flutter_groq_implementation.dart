// Flutter Groq API Service Implementation Guide
// Place this in: flutter_app/lib/services/groq_service.dart

import 'dart:convert';
import 'package:http/http.dart' as http;
import 'package:flutter_dotenv/flutter_dotenv.dart';

class GroqService {
  static const String _baseUrl = 'https://api.groq.com/openai/v1';
  static const String _defaultModel = 'mixtral-8x7b-32768';
  
  // Available models
  static const Map<String, String> models = {
    'mixtral': 'mixtral-8x7b-32768',
    'llama3-70b': 'llama3-70b-8192',
    'llama3-8b': 'llama3-8b-8192',
    'gemma-7b': 'gemma-7b-it',
  };
  
  final String _apiKey;
  final String model;
  
  GroqService({String? apiKey, String? model})
      : _apiKey = apiKey ?? dotenv.env['GROQ_API_KEY'] ?? '',
        model = model ?? _defaultModel {
    if (_apiKey.isEmpty) {
      throw Exception('GROQ_API_KEY not found in environment');
    }
  }
  
  /// Send a chat message to Groq API
  Future<String> chat({
    required String message,
    String? systemPrompt,
    double temperature = 0.7,
    int maxTokens = 1024,
    List<Map<String, String>>? conversationHistory,
  }) async {
    try {
      // Build messages array
      final List<Map<String, String>> messages = [];
      
      // Add system prompt if provided
      if (systemPrompt != null) {
        messages.add({
          'role': 'system',
          'content': systemPrompt,
        });
      }
      
      // Add conversation history if provided
      if (conversationHistory != null) {
        messages.addAll(conversationHistory);
      }
      
      // Add current message
      messages.add({
        'role': 'user',
        'content': message,
      });
      
      // Make API request
      final response = await http.post(
        Uri.parse('$_baseUrl/chat/completions'),
        headers: {
          'Authorization': 'Bearer $_apiKey',
          'Content-Type': 'application/json',
        },
        body: jsonEncode({
          'model': model,
          'messages': messages,
          'temperature': temperature,
          'max_tokens': maxTokens,
        }),
      );
      
      if (response.statusCode == 200) {
        final data = jsonDecode(response.body);
        return data['choices'][0]['message']['content'];
      } else {
        throw Exception('Groq API error: ${response.statusCode} - ${response.body}');
      }
    } catch (e) {
      throw Exception('Failed to send message: $e');
    }
  }
  
  /// Stream chat responses (for real-time typing effect)
  Stream<String> chatStream({
    required String message,
    String? systemPrompt,
    double temperature = 0.7,
    int maxTokens = 1024,
  }) async* {
    try {
      final List<Map<String, String>> messages = [];
      
      if (systemPrompt != null) {
        messages.add({'role': 'system', 'content': systemPrompt});
      }
      
      messages.add({'role': 'user', 'content': message});
      
      final request = http.Request(
        'POST',
        Uri.parse('$_baseUrl/chat/completions'),
      );
      
      request.headers.addAll({
        'Authorization': 'Bearer $_apiKey',
        'Content-Type': 'application/json',
      });
      
      request.body = jsonEncode({
        'model': model,
        'messages': messages,
        'temperature': temperature,
        'max_tokens': maxTokens,
        'stream': true,
      });
      
      final streamedResponse = await request.send();
      
      await for (var chunk in streamedResponse.stream.transform(utf8.decoder)) {
        final lines = chunk.split('\n');
        for (var line in lines) {
          if (line.startsWith('data: ')) {
            final data = line.substring(6);
            if (data == '[DONE]') continue;
            
            try {
              final json = jsonDecode(data);
              if (json['choices'] != null && json['choices'].isNotEmpty) {
                final content = json['choices'][0]['delta']['content'];
                if (content != null) {
                  yield content as String;
                }
              }
            } catch (e) {
              // Skip malformed JSON
              continue;
            }
          }
        }
      }
    } catch (e) {
      throw Exception('Stream error: $e');
    }
  }
}

// Example Usage:
/*

1. Add to pubspec.yaml:
   dependencies:
     http: ^1.2.0
     flutter_dotenv: ^5.1.0

2. Create .env file in flutter_app/:
   GROQ_API_KEY=your_groq_api_key_here

3. Load in main.dart:
   await dotenv.load(fileName: ".env");

4. Use in your app:

// Simple chat
final groq = GroqService();
final response = await groq.chat(
  message: 'Analyze this defect: major crack',
  systemPrompt: 'You are a structural engineer.',
);
print(response);

// Streaming chat
await for (var chunk in groq.chatStream(
  message: 'What causes concrete spalling?',
)) {
  setState(() {
    responseText += chunk;
  });
}

// Defect analysis
final analysis = await groq.chat(
  message: 'Defect: ${defectType}, Location: ${location}',
  systemPrompt: 'You are a building inspector. Provide severity and recommendations.',
  temperature: 0.3,
);

// Generate report
final summary = await groq.chat(
  message: 'Generate inspection summary for: $defectsList',
  systemPrompt: 'Create a professional inspection report.',
  model: GroqService.models['llama3-70b']!,
);

*/
