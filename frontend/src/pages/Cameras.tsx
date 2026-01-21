import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-hot-toast";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { Modal } from "../components/common/Modal";
import { Input } from "../components/common/Input";
import { SkeletonCard } from "../components/common/Skeleton";
import { camerasService, CreateCameraRequest } from "../services/cameras";

export const Cameras: React.FC = () => {
  const queryClient = useQueryClient();
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [formData, setFormData] = useState<CreateCameraRequest>({
    name: "",
    rtsp_url: "",
    location: "",
  });

  const { data: cameras, isLoading } = useQuery({
    queryKey: ["cameras"],
    queryFn: camerasService.getAll,
  });

  const createMutation = useMutation({
    mutationFn: camerasService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cameras"] });
      toast.success("Câmera adicionada com sucesso!");
      setIsModalOpen(false);
      setFormData({ name: "", rtsp_url: "", location: "" });
    },
    onError: () => {
      toast.error("Erro ao adicionar câmera");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: camerasService.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["cameras"] });
      toast.success("Câmera removida com sucesso!");
    },
    onError: () => {
      toast.error("Erro ao remover câmera");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name || !formData.rtsp_url || !formData.location) {
      toast.error("Preencha todos os campos");
      return;
    }
    createMutation.mutate(formData);
  };

  const handleDelete = (id: string, name: string) => {
    if (window.confirm(`Deseja realmente remover a câmera "${name}"?`)) {
      deleteMutation.mutate(id);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Câmeras</h1>
          <p className="text-gray-500 mt-1">Gerenciar câmeras de monitoramento</p>
        </div>
        <Button onClick={() => setIsModalOpen(true)}>
          <span className="mr-2">➕</span>
          Adicionar Câmera
        </Button>
      </div>

      {isLoading ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <SkeletonCard />
          <SkeletonCard />
          <SkeletonCard />
        </div>
      ) : cameras && cameras.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {cameras.map((camera) => (
            <Card key={camera.id} className="hover:shadow-lg transition-shadow">
              <div className="aspect-video bg-gray-900 rounded-lg mb-4 flex items-center justify-center">
                <span className="text-6xl">📹</span>
              </div>
              <div className="space-y-3">
                <div className="flex items-start justify-between">
                  <div>
                    <h3 className="font-semibold text-lg text-gray-900">{camera.name}</h3>
                    <p className="text-sm text-gray-500">{camera.location}</p>
                  </div>
                  <Badge variant={camera.status === "ONLINE" ? "success" : "secondary"}>
                    {camera.status}
                  </Badge>
                </div>
                <div className="flex space-x-2">
                  <Button size="sm" variant="secondary" className="flex-1">
                    Ver Stream
                  </Button>
                  <Button
                    size="sm"
                    variant="danger"
                    onClick={() => handleDelete(camera.id, camera.name)}
                  >
                    Excluir
                  </Button>
                </div>
              </div>
            </Card>
          ))}
        </div>
      ) : (
        <Card>
          <div className="text-center py-12">
            <span className="text-6xl mb-4 block">📹</span>
            <p className="text-gray-500 mb-4">Nenhuma câmera cadastrada</p>
            <Button onClick={() => setIsModalOpen(true)}>Adicionar Primeira Câmera</Button>
          </div>
        </Card>
      )}

      <Modal isOpen={isModalOpen} onClose={() => setIsModalOpen(false)} title="Adicionar Câmera">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Nome da Câmera"
            placeholder="Ex: Câmera Entrada Principal"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
          <Input
            label="URL RTSP ou Webcam"
            placeholder="rtsp://192.168.1.100/stream ou 0 para webcam"
            value={formData.rtsp_url}
            onChange={(e) => setFormData({ ...formData, rtsp_url: e.target.value })}
            helpText="Digite 0 para usar webcam do dispositivo"
            required
          />
          <Input
            label="Localização"
            placeholder="Ex: Portaria Principal"
            value={formData.location}
            onChange={(e) => setFormData({ ...formData, location: e.target.value })}
            required
          />
          <div className="flex space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setIsModalOpen(false)}
              className="flex-1"
            >
              Cancelar
            </Button>
            <Button type="submit" className="flex-1" disabled={createMutation.isPending}>
              {createMutation.isPending ? "Salvando..." : "Salvar"}
            </Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};
