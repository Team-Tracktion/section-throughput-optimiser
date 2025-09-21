"use client";

import { useState } from "react";
import { useAuth } from "../hooks/use-auth";
import { TrainCard } from "./train-card";
import { Button } from "./ui/button";
import { Input } from "./ui/input";
import { LogOut, Search, RefreshCw, Train, Clock, MapPin } from "lucide-react";

// Mock train data - replace with Firebase API calls
const mockTrains = [
  {
    id: "1",
    number: "TN-12345",
    name: "Chennai Express",
    route: "Chennai Central → Bangalore",
    status: "on-time",
    departureTime: "14:30",
    currentStation: "Katpadi Junction",
    location: "Platform 2",
    eta: "16:45",
  },
  {
    id: "2",
    number: "TN-67890",
    name: "Coromandel Express",
    route: "Chennai → Howrah",
    status: "delayed",
    departureTime: "15:15",
    currentStation: "Arakkonam",
    location: "En Route",
    eta: "17:30",
  },
  {
    id: "3",
    number: "TN-11111",
    name: "Shatabdi Express",
    route: "Chennai → Mysore",
    status: "halted",
    departureTime: "16:00",
    currentStation: "Jolarpettai",
    location: "Platform 1",
    eta: "18:15",
  },
];

export function Dashboard() {
  const { user, logout } = useAuth();
  const [trains, setTrains] = useState(mockTrains);
  const [searchTerm, setSearchTerm] = useState("");
  const [statusFilter, setStatusFilter] = useState("all");
  const [loading, setLoading] = useState(false);

  const filteredTrains = trains.filter((train) => {
    const matchesSearch =
      train.number.toLowerCase().includes(searchTerm.toLowerCase()) ||
      train.name.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesStatus =
      statusFilter === "all" || train.status === statusFilter;
    return matchesSearch && matchesStatus;
  });

  const handleHalt = (trainId) => {
    setTrains(
      trains.map((train) =>
        train.id === trainId ? { ...train, status: "halted" } : train
      )
    );
  };

  const handleLetGo = (trainId) => {
    setTrains(
      trains.map((train) =>
        train.id === trainId ? { ...train, status: "on-time" } : train
      )
    );
  };

  const handleRefresh = () => {
    setLoading(true);
    // Simulate API call
    setTimeout(() => {
      setLoading(false);
    }, 1000);
  };

  const getStatusCount = (status) => {
    return trains.filter((train) => train.status === status).length;
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b bg-card">
        <div className="container mx-auto px-4 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="p-2 bg-primary/10 rounded-lg">
                <Train className="h-6 w-6 text-primary" />
              </div>
              <div>
                <h1 className="text-xl font-bold">Railway Control System</h1>
                <p className="text-sm text-muted-foreground">Chennai Section</p>
              </div>
            </div>

            <div className="flex items-center gap-3">
              <span className="text-sm text-muted-foreground">
                Welcome, {user?.email.split("@gmail.com")[0]}
              </span>
              <Button variant="outline" size="sm" onClick={logout}>
                <LogOut className="h-4 w-4 mr-2" />
                Logout
              </Button>
            </div>
          </div>
        </div>
      </header>

      <main className="container mx-auto px-4 py-6">
        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
          <div className="bg-card p-4 rounded-lg border">
            <div className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-success" />
              <div>
                <div className="text-2xl font-bold">
                  {getStatusCount("on-time")}
                </div>
                <div className="text-sm text-muted-foreground">On Time</div>
              </div>
            </div>
          </div>

          <div className="bg-card p-4 rounded-lg border">
            <div className="flex items-center gap-2">
              <Clock className="h-5 w-5 text-warning" />
              <div>
                <div className="text-2xl font-bold">
                  {getStatusCount("delayed")}
                </div>
                <div className="text-sm text-muted-foreground">Delayed</div>
              </div>
            </div>
          </div>

          <div className="bg-card p-4 rounded-lg border">
            <div className="flex items-center gap-2">
              <MapPin className="h-5 w-5 text-destructive" />
              <div>
                <div className="text-2xl font-bold">
                  {getStatusCount("halted")}
                </div>
                <div className="text-sm text-muted-foreground">Halted</div>
              </div>
            </div>
          </div>

          <div className="bg-card p-4 rounded-lg border">
            <div className="flex items-center gap-2">
              <Train className="h-5 w-5 text-primary" />
              <div>
                <div className="text-2xl font-bold">{trains.length}</div>
                <div className="text-sm text-muted-foreground">
                  Total Trains
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Controls */}
        <div className="flex flex-col sm:flex-row gap-4 mb-6">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-4 w-4 text-muted-foreground" />
            <Input
              placeholder="Search trains..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10"
            />
          </div>

          <div className="flex gap-2">
            <Button
              variant={statusFilter === "all" ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter("all")}
            >
              All
            </Button>
            <Button
              variant={statusFilter === "on-time" ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter("on-time")}
            >
              On Time
            </Button>
            <Button
              variant={statusFilter === "delayed" ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter("delayed")}
            >
              Delayed
            </Button>
            <Button
              variant={statusFilter === "halted" ? "default" : "outline"}
              size="sm"
              onClick={() => setStatusFilter("halted")}
            >
              Halted
            </Button>
          </div>

          <Button
            variant="outline"
            size="sm"
            onClick={handleRefresh}
            disabled={loading}
          >
            <RefreshCw
              className={`h-4 w-4 mr-2 ${loading ? "animate-spin" : ""}`}
            />
            Refresh
          </Button>
        </div>

        {/* Train List */}
        <div className="space-y-4">
          {filteredTrains.map((train) => (
            <TrainCard
              key={train.id}
              train={train}
              onHalt={handleHalt}
              onLetGo={handleLetGo}
            />
          ))}

          {filteredTrains.length === 0 && (
            <div className="text-center py-12">
              <Train className="h-12 w-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-medium mb-2">No trains found</h3>
              <p className="text-muted-foreground">
                Try adjusting your search or filter criteria.
              </p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
