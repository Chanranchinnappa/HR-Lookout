'use client';

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { organizationsApi, employeesApi, departmentsApi } from '@/lib/api';

interface Stats {
  totalOrganizations: number;
  totalEmployees: number;
  activeEmployees: number;
  onLeaveEmployees: number;
  inactiveEmployees: number;
  terminatedEmployees: number;
  totalDepartments: number;
  systemStatus: string;
}

export default function Home() {
  const [stats, setStats] = useState<Stats>({
    totalOrganizations: 0,
    totalEmployees: 0,
    activeEmployees: 0,
    onLeaveEmployees: 0,
    inactiveEmployees: 0,
    terminatedEmployees: 0,
    totalDepartments: 0,
    systemStatus: 'All Systems Operational',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      setLoading(true);
      setError(null);

      // FIXED: Changed employment_status to status
      const [orgsRes, empsRes, activeRes, onLeaveRes, inactiveRes, terminatedRes, deptsRes] = await Promise.all([
        organizationsApi.getAll(),
        employeesApi.getAll(),
        employeesApi.getAll({ status: 'ACTIVE' }),
        employeesApi.getAll({ status: 'ON_LEAVE' }),
        employeesApi.getAll({ status: 'INACTIVE' }),
        employeesApi.getAll({ status: 'TERMINATED' }),
        departmentsApi.getAll(),
      ]);

      setStats({
        totalOrganizations: orgsRes.data.count || 0,
        totalEmployees: empsRes.data.count || 0,
        activeEmployees: activeRes.data.count || 0,
        onLeaveEmployees: onLeaveRes.data.count || 0,
        inactiveEmployees: inactiveRes.data.count || 0,
        terminatedEmployees: terminatedRes.data.count || 0,
        totalDepartments: deptsRes.data.count || 0,
        systemStatus: 'All Systems Operational',
      });
      
      setLoading(false);
    } catch (err: any) {
      console.error('Error fetching stats:', err);
      setError('Failed to load dashboard stats');
      setLoading(false);
    }
  };

  // Filter status cards - only show if count > 0
  const statusCards = [
    {
      label: 'Active',
      count: stats.activeEmployees,
      status: 'ACTIVE',
      gradient: 'from-emerald-600 to-emerald-700',
      hoverShadow: 'hover:shadow-emerald-500/50',
      icon: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z',
      textColor: 'text-emerald-100',
      bgColor: 'bg-emerald-500/30',
    },
    {
      label: 'On Leave',
      count: stats.onLeaveEmployees,
      status: 'ON_LEAVE',
      gradient: 'from-yellow-600 to-yellow-700',
      hoverShadow: 'hover:shadow-yellow-500/50',
      icon: 'M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z',
      textColor: 'text-yellow-100',
      bgColor: 'bg-yellow-500/30',
    },
    {
      label: 'Inactive',
      count: stats.inactiveEmployees,
      status: 'INACTIVE',
      gradient: 'from-gray-600 to-gray-700',
      hoverShadow: 'hover:shadow-gray-500/50',
      icon: 'M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L5.636 5.636',
      textColor: 'text-gray-100',
      bgColor: 'bg-gray-500/30',
    },
    {
      label: 'Terminated',
      count: stats.terminatedEmployees,
      status: 'TERMINATED',
      gradient: 'from-red-600 to-red-700',
      hoverShadow: 'hover:shadow-red-500/50',
      icon: 'M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z',
      textColor: 'text-red-100',
      bgColor: 'bg-red-500/30',
    },
  ].filter(card => card.count > 0); // Only show cards with employees

  if (error) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
        <div className="text-center">
          <div className="text-red-400 text-xl mb-4">{error}</div>
          <button
            onClick={fetchStats}
            className="px-6 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-5xl font-bold text-white mb-3 drop-shadow-2xl">
            Welcome to HR-Lookout
          </h1>
          <p className="text-gray-300 text-lg">
            Your comprehensive HR management dashboard
          </p>
        </div>

        {/* ROW 1: Organizations & Departments - Large Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
          {/* Organizations Card */}
          <Link href="/organizations">
            <div className="bg-gradient-to-br from-blue-600 to-blue-700 rounded-2xl p-8 shadow-2xl hover:shadow-blue-500/50 transition-all hover:scale-105 cursor-pointer">
              <div className="flex items-center justify-between mb-6">
                <div className="text-blue-100 text-sm font-semibold uppercase tracking-wider">
                  Organizations
                </div>
                <div className="bg-blue-500/30 p-3 rounded-xl">
                  <svg
                    className="w-8 h-8 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                    />
                  </svg>
                </div>
              </div>
              <div className="text-6xl font-bold text-white mb-4">
                {loading ? <span className="animate-pulse">...</span> : stats.totalOrganizations}
              </div>
              <div className="text-blue-100 hover:text-white text-sm font-medium flex items-center gap-1 transition">
                View all organizations →
              </div>
            </div>
          </Link>

          {/* Departments Card */}
          <Link href="/departments">
            <div className="bg-gradient-to-br from-amber-600 to-amber-700 rounded-2xl p-8 shadow-2xl hover:shadow-amber-500/50 transition-all hover:scale-105 cursor-pointer">
              <div className="flex items-center justify-between mb-6">
                <div className="text-amber-100 text-sm font-semibold uppercase tracking-wider">
                  Departments
                </div>
                <div className="bg-amber-500/30 p-3 rounded-xl">
                  <svg
                    className="w-8 h-8 text-white"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M4 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1H5a1 1 0 01-1-1V5zM14 5a1 1 0 011-1h4a1 1 0 011 1v7a1 1 0 01-1 1h-4a1 1 0 01-1-1V5zM4 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1H5a1 1 0 01-1-1v-3zM14 16a1 1 0 011-1h4a1 1 0 011 1v3a1 1 0 01-1 1h-4a1 1 0 01-1-1v-3z"
                    />
                  </svg>
                </div>
              </div>
              <div className="text-6xl font-bold text-white mb-4">
                {loading ? <span className="animate-pulse">...</span> : stats.totalDepartments}
              </div>
              <div className="text-amber-100 hover:text-white text-sm font-medium flex items-center gap-1 transition">
                View all departments →
              </div>
            </div>
          </Link>
        </div>

        {/* ROW 2: Employee Status Breakdown - Dynamic columns based on count */}
        {statusCards.length > 0 && (
          <div className={`grid grid-cols-2 md:grid-cols-${Math.min(statusCards.length, 4)} gap-4 mb-8`}>
            {statusCards.map((card) => (
              <Link key={card.status} href={`/employees?status=${card.status}`}>
                <div className={`bg-gradient-to-br ${card.gradient} rounded-xl p-5 shadow-xl ${card.hoverShadow} transition-all hover:scale-105 cursor-pointer`}>
                  <div className="flex items-center justify-between mb-3">
                    <div className={`${card.textColor} text-xs font-semibold uppercase tracking-wider`}>
                      {card.label}
                    </div>
                    <div className={`${card.bgColor} p-2 rounded-lg`}>
                      <svg
                        className="w-5 h-5 text-white"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d={card.icon}
                        />
                      </svg>
                    </div>
                  </div>
                  <div className="text-4xl font-bold text-white mb-2">
                    {loading ? <span className="animate-pulse">...</span> : card.count}
                  </div>
                  <div className={`${card.textColor} text-xs`}>Employees</div>
                </div>
              </Link>
            ))}
          </div>
        )}

        {/* Total Employees Summary */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-gray-700 rounded-xl p-4 mb-8 shadow-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <svg
                className="w-6 h-6 text-blue-400"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
                />
              </svg>
              <span className="text-white font-semibold">
                Total Employees: {loading ? '...' : stats.totalEmployees}
              </span>
            </div>
            <Link
              href="/employees"
              className="text-blue-400 hover:text-blue-300 text-sm font-medium flex items-center gap-1"
            >
              View All →
            </Link>
          </div>
        </div>

        {/* System Status */}
        <div className="bg-slate-800/50 backdrop-blur-sm border border-gray-700 rounded-2xl p-6 mb-8 shadow-xl">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
              <span className="text-white font-semibold text-lg">{stats.systemStatus}</span>
            </div>
            <div className="text-gray-400 text-sm">
              Last checked: {new Date().toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' })}
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Link
            href="/employees/new"
            className="bg-gradient-to-r from-blue-600 to-cyan-600 rounded-2xl p-6 shadow-2xl hover:shadow-blue-500/50 transition-all hover:scale-105 group"
          >
            <div className="flex items-center gap-4">
              <div className="bg-white/20 p-3 rounded-xl group-hover:bg-white/30 transition">
                <svg
                  className="w-7 h-7 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M18 9v3m0 0v3m0-3h3m-3 0h-3m-2-5a4 4 0 11-8 0 4 4 0 018 0zM3 20a6 6 0 0112 0v1H3v-1z"
                  />
                </svg>
              </div>
              <div>
                <h3 className="text-white text-lg font-bold mb-1">Add Employee</h3>
                <p className="text-blue-100 text-xs">Create new record</p>
              </div>
            </div>
          </Link>

          <Link
            href="/departments/new"
            className="bg-gradient-to-r from-purple-600 to-pink-600 rounded-2xl p-6 shadow-2xl hover:shadow-purple-500/50 transition-all hover:scale-105 group"
          >
            <div className="flex items-center gap-4">
              <div className="bg-white/20 p-3 rounded-xl group-hover:bg-white/30 transition">
                <svg
                  className="w-7 h-7 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 6v6m0 0v6m0-6h6m-6 0H6"
                  />
                </svg>
              </div>
              <div>
                <h3 className="text-white text-lg font-bold mb-1">Add Department</h3>
                <p className="text-purple-100 text-xs">Create new department</p>
              </div>
            </div>
          </Link>

          <Link
            href="/organizations/new"
            className="bg-gradient-to-r from-violet-600 to-indigo-600 rounded-2xl p-6 shadow-2xl hover:shadow-violet-500/50 transition-all hover:scale-105 group"
          >
            <div className="flex items-center gap-4">
              <div className="bg-white/20 p-3 rounded-xl group-hover:bg-white/30 transition">
                <svg
                  className="w-7 h-7 text-white"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4"
                  />
                </svg>
              </div>
              <div>
                <h3 className="text-white text-lg font-bold mb-1">Add Organization</h3>
                <p className="text-violet-100 text-xs">Register new org</p>
              </div>
            </div>
          </Link>
        </div>
      </div>
    </div>
  );
}
