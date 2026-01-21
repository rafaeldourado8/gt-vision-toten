"""
Script para gerar vídeo de teste com rostos simulados
"""
import cv2
import numpy as np
from pathlib import Path

def create_test_video(output_path: str, duration_seconds: int = 30, fps: int = 30):
    """Cria um vídeo de teste com rostos simulados"""
    
    width, height = 640, 480
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    total_frames = duration_seconds * fps
    
    print(f"Gerando vídeo de teste: {output_path}")
    print(f"Duração: {duration_seconds}s | FPS: {fps} | Frames: {total_frames}")
    
    for frame_num in range(total_frames):
        # Fundo azul
        frame = np.ones((height, width, 3), dtype=np.uint8) * 50
        
        # Simula movimento de pessoa
        x = int((frame_num / total_frames) * width)
        y = height // 2
        
        # Desenha "pessoa" (círculo para cabeça + retângulo para corpo)
        cv2.circle(frame, (x, y - 50), 40, (200, 180, 150), -1)  # Cabeça
        cv2.rectangle(frame, (x - 30, y - 10), (x + 30, y + 80), (100, 100, 200), -1)  # Corpo
        
        # Adiciona olhos
        cv2.circle(frame, (x - 15, y - 60), 5, (0, 0, 0), -1)
        cv2.circle(frame, (x + 15, y - 60), 5, (0, 0, 0), -1)
        
        # Adiciona texto
        cv2.putText(frame, f"Frame: {frame_num}", (10, 30), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.putText(frame, "Test Video - GT-Vision", (10, height - 20),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        out.write(frame)
        
        if frame_num % 30 == 0:
            print(f"Progresso: {frame_num}/{total_frames} frames")
    
    out.release()
    print(f"✓ Vídeo criado: {output_path}")

if __name__ == "__main__":
    output_dir = Path(__file__).parent / "videos"
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / "test_video.mp4"
    create_test_video(str(output_file), duration_seconds=30, fps=30)
