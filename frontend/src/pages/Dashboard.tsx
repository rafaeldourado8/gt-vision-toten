import React from "react";
import { useQuery } from "@tanstack/react-query";
import { Card } from "../components/common/Card";
import { Badge } from "../components/common/Badge";
import { Avatar } from "../components/common/Avatar";
import { SkeletonCard, SkeletonTable } from "../components/common/Skeleton";
import { dashboardService } from "../services/dashboard";

export const Dashboard: React.FC = () => {
  const { data: stats, isLoading: statsLoading } = useQuery({
    queryKey: ["dashboard-stats"],
    queryFn: dashboardService.getStats,
  });

  const { data: chartData, isLoading: chartLoading } = useQuery({
    queryKey: ["attendance-chart"],
    queryFn: dashboardService.getAttendanceChart,
  });

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-500 mt-1">Visão geral do sistema de presença</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsLoading ? (
          <>
            <SkeletonCard />
            <SkeletonCard />
            <SkeletonCard />
            <SkeletonCard />
          </>
        ) : (
          <>
            <Card className="bg-gradient-to-br from-blue-50 to-white border-blue-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Total de Alunos</p>
                  <p className="text-3xl font-bold text-gray-900">{stats?.total_students || 0}</p>
                </div>
                <div className="text-4xl">👥</div>
              </div>
            </Card>

            <Card className="bg-gradient-to-br from-green-50 to-white border-green-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Câmeras Online</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stats?.cameras_online || 0}/{stats?.total_cameras || 0}
                  </p>
                </div>
                <div className="text-4xl">📹</div>
              </div>
            </Card>

            <Card className="bg-gradient-to-br from-emerald-50 to-white border-emerald-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Presentes Hoje</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stats?.today_attendance.present || 0}
                  </p>
                </div>
                <div className="text-4xl">✅</div>
              </div>
            </Card>

            <Card className="bg-gradient-to-br from-red-50 to-white border-red-100">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-gray-600 mb-1">Ausentes Hoje</p>
                  <p className="text-3xl font-bold text-gray-900">
                    {stats?.today_attendance.absent || 0}
                  </p>
                </div>
                <div className="text-4xl">❌</div>
              </div>
            </Card>
          </>
        )}
      </div>

      {/* Attendance Chart */}
      <Card title="Presença dos Últimos 7 Dias">
        {chartLoading ? (
          <div className="h-64 flex items-center justify-center">
            <p className="text-gray-400">Carregando gráfico...</p>
          </div>
        ) : (
          <div className="h-64">
            <div className="flex items-end justify-between h-full space-x-2">
              {chartData?.labels.map((label, index) => {
                const total =
                  (chartData.present[index] || 0) +
                  (chartData.late[index] || 0) +
                  (chartData.absent[index] || 0);
                const presentHeight = total > 0 ? (chartData.present[index] / total) * 100 : 0;
                const lateHeight = total > 0 ? (chartData.late[index] / total) * 100 : 0;
                const absentHeight = total > 0 ? (chartData.absent[index] / total) * 100 : 0;

                return (
                  <div key={index} className="flex-1 flex flex-col items-center">
                    <div className="w-full flex flex-col-reverse h-48 space-y-reverse space-y-1">
                      <div
                        className="w-full bg-green-500 rounded-t transition-all"
                        style={{ height: `${presentHeight}%` }}
                        title={`Presentes: ${chartData.present[index]}`}
                      />
                      <div
                        className="w-full bg-yellow-500 transition-all"
                        style={{ height: `${lateHeight}%` }}
                        title={`Atrasados: ${chartData.late[index]}`}
                      />
                      <div
                        className="w-full bg-red-500 transition-all"
                        style={{ height: `${absentHeight}%` }}
                        title={`Ausentes: ${chartData.absent[index]}`}
                      />
                    </div>
                    <p className="text-xs text-gray-600 mt-2">{label}</p>
                  </div>
                );
              })}
            </div>
            <div className="flex items-center justify-center space-x-6 mt-6 pt-4 border-t border-gray-200">
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-green-500 rounded" />
                <span className="text-sm text-gray-600">Presentes</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-yellow-500 rounded" />
                <span className="text-sm text-gray-600">Atrasados</span>
              </div>
              <div className="flex items-center space-x-2">
                <div className="w-4 h-4 bg-red-500 rounded" />
                <span className="text-sm text-gray-600">Ausentes</span>
              </div>
            </div>
          </div>
        )}
      </Card>

      {/* Last Detections */}
      <Card title="Últimas Detecções">
        {statsLoading ? (
          <SkeletonTable rows={5} />
        ) : stats?.last_detections && stats.last_detections.length > 0 ? (
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Aluno
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Horário
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Câmera
                  </th>
                  <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">
                    Status
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {stats.last_detections.map((detection, index) => (
                  <tr key={index} className="hover:bg-gray-50">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="flex items-center">
                        <Avatar name={detection.student_name} size="sm" />
                        <span className="ml-3 text-sm font-medium text-gray-900">
                          {detection.student_name}
                        </span>
                      </div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {new Date(detection.timestamp).toLocaleTimeString("pt-BR")}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                      {detection.camera}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <Badge
                        variant={
                          detection.status === "PRESENT"
                            ? "success"
                            : detection.status === "LATE"
                            ? "warning"
                            : "danger"
                        }
                      >
                        {detection.status === "PRESENT"
                          ? "Presente"
                          : detection.status === "LATE"
                          ? "Atrasado"
                          : "Ausente"}
                      </Badge>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        ) : (
          <div className="text-center py-12">
            <p className="text-gray-500">Nenhuma detecção registrada hoje</p>
          </div>
        )}
      </Card>
    </div>
  );
};
