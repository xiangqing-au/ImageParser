# EasyOCR GPU Setup Guide

This guide applies only when using the optional EasyOCR backend. The example
configuration uses Tesseract with `ocr_gpu: false`; Tesseract does not use this
GPU setting.

## CUDA setup (Linux/Windows with a supported NVIDIA GPU)

Install a PyTorch build compatible with your CUDA driver. For example:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121
```

Or use conda:
```bash
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
```

Install ImageParser's EasyOCR extra in the same environment:

```bash
python -m pip install -e ".[easyocr]"
```

Verify CUDA availability:
```bash
python -c "import torch; print('CUDA available:', torch.cuda.is_available()); print('GPU:', torch.cuda.get_device_name(0) if torch.cuda.is_available() else 'N/A')"
```

Set `ocr_engine: easyocr` and `ocr_gpu: true` in the active configuration to
request GPU acceleration. Availability depends on the operating system,
PyTorch build, and supported hardware.

Without a supported GPU, use `ocr_gpu: false` or select
`ocr_engine: tesseract`.
