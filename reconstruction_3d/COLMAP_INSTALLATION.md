# 🔧 COLMAP Installation Guide for Windows

## Quick Install (Recommended)

### Option 1: Pre-built Binaries (Easiest)

1. **Download COLMAP**:
   - Visit: https://github.com/colmap/colmap/releases
   - Download latest Windows build: `COLMAP-X.X-windows-cuda.zip` or `COLMAP-X.X-windows-no-cuda.zip`

2. **Extract**:
   ```powershell
   # Extract to C:\Program Files\COLMAP
   # Or any location you prefer
   ```

3. **Add to PATH**:
   ```powershell
   # Open PowerShell as Administrator
   $env:Path += ";C:\Program Files\COLMAP"
   
   # Make it permanent
   [System.Environment]::SetEnvironmentVariable(
       "Path",
       [System.Environment]::GetEnvironmentVariable("Path", "Machine") + ";C:\Program Files\COLMAP",
       "Machine"
   )
   ```

4. **Verify Installation**:
   ```powershell
   colmap -h
   # Should show COLMAP help message
   ```

### Option 2: Conda Install (If you use Conda)

```bash
conda install -c conda-forge colmap
```

## Configure SiteLenz

If COLMAP is not in PATH, specify full path in code:

```python
# In reconstruction_3d/api/routes.py, line ~250
colmap = COLMAPWrapper(
    workspace_path=str(session_folder),
    colmap_exe="C:/Program Files/COLMAP/colmap.exe"  # <-- Change this
)
```

## GPU Acceleration (Optional but Recommended)

### Requirements:
- NVIDIA GPU
- CUDA Toolkit 11.0 or newer
- cuDNN library

### Check if GPU is available:
```powershell
nvidia-smi
```

If you have an NVIDIA GPU, download the CUDA version of COLMAP for 10x faster processing!

## Test COLMAP Installation

Run this command to test:

```powershell
cd e:\projects\major_project
python -c "from reconstruction_3d.colmap.colmap_wrapper import COLMAPWrapper; c = COLMAPWrapper('test', 'colmap'); print('✅ COLMAP integration working!')"
```

## Troubleshooting

### "colmap is not recognized"

**Solution 1**: Add to PATH manually
- Right-click "This PC" → Properties → Advanced System Settings
- Environment Variables → System Variables → Path → Edit
- Add: `C:\Program Files\COLMAP`

**Solution 2**: Use full path in config.py
```python
# reconstruction_3d/config.py
COLMAP_EXE = "C:/Program Files/COLMAP/colmap.exe"
```

### "CUDA not found" or GPU errors

- Download CPU-only version (slower but works)
- Or install CUDA Toolkit from: https://developer.nvidia.com/cuda-downloads

### Missing DLL errors

Install Visual C++ Redistributables:
- https://aka.ms/vs/17/release/vc_redist.x64.exe

## Alternative: Use COLMAP Online (No Installation)

If you can't install COLMAP locally, you can:
1. Use cloud services like Google Colab
2. Install on a server and expose API
3. Use alternative reconstruction libraries (meshroom, openMVG)

## Next Steps

Once COLMAP is installed:

1. Start Flask server:
   ```powershell
   python app.py
   ```

2. Test 3D endpoint:
   ```powershell
   curl http://localhost:5000/api/3d/start-session -X POST -H "Content-Type: application/json" -d "{\"project_name\":\"test\"}"
   ```

3. Check logs for any COLMAP errors

## Performance Tips

- **Use GPU version**: 10-20x faster
- **SSD storage**: Much faster I/O
- **Close other apps**: COLMAP is memory-intensive
- **Start with 'low' quality**: Test before running high quality

## System Requirements

### Minimum:
- Windows 10/11
- 8GB RAM
- 2GB free disk space per reconstruction
- Any CPU from last 5 years

### Recommended:
- Windows 10/11
- 16GB+ RAM
- NVIDIA GPU with 4GB+ VRAM
- SSD with 10GB+ free space
- Intel i7/AMD Ryzen 7 or better

## Need Help?

Check the logs:
1. Flask console output
2. `reconstruction_3d/sessions/<session_id>/`
3. COLMAP documentation: https://colmap.github.io/

---

**Ready to create 3D models!** 🎉
