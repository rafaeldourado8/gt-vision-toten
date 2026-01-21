import React, { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { toast } from "react-hot-toast";
import { Card } from "../components/common/Card";
import { Button } from "../components/common/Button";
import { Badge } from "../components/common/Badge";
import { Avatar } from "../components/common/Avatar";
import { Modal } from "../components/common/Modal";
import { Input } from "../components/common/Input";
import { Table } from "../components/common/Table";
import { SkeletonTable } from "../components/common/Skeleton";
import { studentsService, CreateStudentRequest, Student } from "../services/students";

export const Students: React.FC = () => {
  const queryClient = useQueryClient();
  const [isAddModalOpen, setIsAddModalOpen] = useState(false);
  const [isPhotoModalOpen, setIsPhotoModalOpen] = useState(false);
  const [selectedStudent, setSelectedStudent] = useState<Student | null>(null);
  const [searchTerm, setSearchTerm] = useState("");
  const [photoFile, setPhotoFile] = useState<File | null>(null);
  const [photoPreview, setPhotoPreview] = useState<string>("");
  const [formData, setFormData] = useState<CreateStudentRequest>({
    name: "",
    grade: "",
    section: "",
  });

  const { data: students, isLoading } = useQuery({
    queryKey: ["students"],
    queryFn: studentsService.getAll,
  });

  const createMutation = useMutation({
    mutationFn: studentsService.create,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["students"] });
      toast.success("Aluno adicionado com sucesso!");
      setIsAddModalOpen(false);
      setFormData({ name: "", grade: "", section: "" });
    },
    onError: () => {
      toast.error("Erro ao adicionar aluno");
    },
  });

  const deleteMutation = useMutation({
    mutationFn: studentsService.delete,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["students"] });
      toast.success("Aluno removido com sucesso!");
    },
    onError: () => {
      toast.error("Erro ao remover aluno");
    },
  });

  const uploadPhotoMutation = useMutation({
    mutationFn: ({ id, photo }: { id: string; photo: File }) =>
      studentsService.uploadPhoto(id, photo),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["students"] });
      toast.success("Foto processada com sucesso!");
      setIsPhotoModalOpen(false);
      setPhotoFile(null);
      setPhotoPreview("");
      setSelectedStudent(null);
    },
    onError: () => {
      toast.error("Erro ao processar foto");
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!formData.name || !formData.grade || !formData.section) {
      toast.error("Preencha todos os campos");
      return;
    }
    createMutation.mutate(formData);
  };

  const handlePhotoChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setPhotoFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setPhotoPreview(reader.result as string);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleUploadPhoto = () => {
    if (!selectedStudent || !photoFile) {
      toast.error("Selecione uma foto");
      return;
    }
    uploadPhotoMutation.mutate({ id: selectedStudent.id, photo: photoFile });
  };

  const handleDelete = (id: string, name: string) => {
    if (window.confirm(`Deseja realmente remover o aluno "${name}"?`)) {
      deleteMutation.mutate(id);
    }
  };

  const openPhotoModal = (student: Student) => {
    setSelectedStudent(student);
    setIsPhotoModalOpen(true);
  };

  const filteredStudents = students?.filter((student) =>
    student.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const columns = [
    {
      key: "avatar",
      label: "Foto",
      render: (student: Student) => <Avatar name={student.name} size="sm" />,
    },
    {
      key: "name",
      label: "Nome",
    },
    {
      key: "class_room",
      label: "Turma",
    },
    {
      key: "face_status",
      label: "Status Face",
      render: (student: Student) => (
        <Badge variant={student.has_face_profile ? "success" : "secondary"}>
          {student.has_face_profile ? "✅ Com foto" : "❌ Sem foto"}
        </Badge>
      ),
    },
    {
      key: "actions",
      label: "Ações",
      render: (student: Student) => (
        <div className="flex space-x-2">
          <Button size="sm" variant="secondary" onClick={() => openPhotoModal(student)}>
            Upload Foto
          </Button>
          <Button
            size="sm"
            variant="danger"
            onClick={() => handleDelete(student.id, student.name)}
          >
            Excluir
          </Button>
        </div>
      ),
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Alunos</h1>
          <p className="text-gray-500 mt-1">Gerenciar cadastro de alunos</p>
        </div>
        <Button onClick={() => setIsAddModalOpen(true)}>
          <span className="mr-2">➕</span>
          Adicionar Aluno
        </Button>
      </div>

      <Card>
        <div className="mb-4">
          <Input
            placeholder="Buscar aluno por nome..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>

        {isLoading ? (
          <SkeletonTable rows={5} />
        ) : filteredStudents && filteredStudents.length > 0 ? (
          <Table columns={columns} data={filteredStudents} />
        ) : (
          <div className="text-center py-12">
            <span className="text-6xl mb-4 block">🎓</span>
            <p className="text-gray-500 mb-4">
              {searchTerm ? "Nenhum aluno encontrado" : "Nenhum aluno cadastrado"}
            </p>
            {!searchTerm && (
              <Button onClick={() => setIsAddModalOpen(true)}>Adicionar Primeiro Aluno</Button>
            )}
          </div>
        )}
      </Card>

      {/* Add Student Modal */}
      <Modal isOpen={isAddModalOpen} onClose={() => setIsAddModalOpen(false)} title="Adicionar Aluno">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Input
            label="Nome Completo"
            placeholder="Ex: João Silva Santos"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            required
          />
          <Input
            label="Série"
            placeholder="Ex: 5º Ano"
            value={formData.grade}
            onChange={(e) => setFormData({ ...formData, grade: e.target.value })}
            required
          />
          <Input
            label="Turma"
            placeholder="Ex: A"
            value={formData.section}
            onChange={(e) => setFormData({ ...formData, section: e.target.value })}
            required
          />
          <div className="flex space-x-3 pt-4">
            <Button
              type="button"
              variant="secondary"
              onClick={() => setIsAddModalOpen(false)}
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

      {/* Upload Photo Modal */}
      <Modal
        isOpen={isPhotoModalOpen}
        onClose={() => {
          setIsPhotoModalOpen(false);
          setPhotoFile(null);
          setPhotoPreview("");
          setSelectedStudent(null);
        }}
        title={`Upload de Foto - ${selectedStudent?.name}`}
      >
        <div className="space-y-4">
          <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
            {photoPreview ? (
              <div className="space-y-4">
                <img
                  src={photoPreview}
                  alt="Preview"
                  className="max-h-64 mx-auto rounded-lg"
                />
                <Button
                  variant="secondary"
                  size="sm"
                  onClick={() => {
                    setPhotoFile(null);
                    setPhotoPreview("");
                  }}
                >
                  Trocar Foto
                </Button>
              </div>
            ) : (
              <div>
                <span className="text-6xl mb-4 block">📸</span>
                <p className="text-gray-600 mb-4">Clique para selecionar uma foto</p>
                <input
                  type="file"
                  accept="image/jpeg,image/png"
                  onChange={handlePhotoChange}
                  className="hidden"
                  id="photo-upload"
                />
                <label htmlFor="photo-upload">
                  <Button as="span" variant="secondary">
                    Selecionar Arquivo
                  </Button>
                </label>
              </div>
            )}
          </div>
          <div className="flex space-x-3">
            <Button
              type="button"
              variant="secondary"
              onClick={() => {
                setIsPhotoModalOpen(false);
                setPhotoFile(null);
                setPhotoPreview("");
                setSelectedStudent(null);
              }}
              className="flex-1"
            >
              Cancelar
            </Button>
            <Button
              onClick={handleUploadPhoto}
              className="flex-1"
              disabled={!photoFile || uploadPhotoMutation.isPending}
            >
              {uploadPhotoMutation.isPending ? "Processando..." : "Processar Face"}
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  );
};
