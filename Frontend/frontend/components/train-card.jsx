"use client";

import { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "./ui/card";
import { Badge } from "./ui/badge";
import { Button } from "./ui/button";
import {
  ChevronDown,
  ChevronUp,
  Clock,
  MapPin,
  Navigation,
  Pause,
  Play,
  AlertTriangle,
  Route,
  Timer,
  Train,
} from "lucide-react";
import { cn } from "../lib/utils";

function RouteVisualization({ train }) {
  // Sample route data - in real app this would come from API
  const routeStations = Array.isArray(train.route)
    ? train.route
    : [
        {
          code: "PUNE",
          name: "Pune Junction",
          arrival: "Start",
          departure: train.departureTime,
          distance: 0,
          status: "completed",
          platform: "PF 1",
        },
        {
          code: "DD",
          name: "Daund Junction",
          arrival: "07:45",
          departure: "07:50",
          distance: 72,
          status: "completed",
          platform: "PF 2",
        },
        {
          code: "ANG",
          name: "Ahmednagar",
          arrival: "09:15",
          departure: "09:20",
          distance: 154,
          status: "current",
          platform: "PF 1",
        },
        {
          code: "MMR",
          name: "Manmad Junction",
          arrival: "11:30",
          departure: "11:35",
          distance: 307,
          status: "upcoming",
          platform: "PF 3",
        },
        {
          code: "BSL",
          name: "Bhusaval Junction",
          arrival: "13:45",
          departure: "13:50",
          distance: 481,
          status: "upcoming",
          platform: "PF 2",
        },
        {
          code: "MKU",
          name: "Malkapur",
          arrival: "14:30",
          departure: "14:32",
          distance: 541,
          status: "upcoming",
          platform: "PF 1",
        },
        {
          code: "NGP",
          name: "Nagpur Junction",
          arrival: train.estimatedArrival,
          departure: "End",
          distance: 849,
          status: "upcoming",
          platform: "PF 4",
        },
      ];

  const calculateTrainPosition = () => {
    const stationsArr = Array.isArray(routeStations) ? routeStations : [];
    if (stationsArr.length === 0) return 0;
    const totalDistance = stationsArr[stationsArr.length - 1].distance;
    const currentStation = stationsArr.find(
      (station) => station.status === "current"
    );

    if (!currentStation) return 0;

    // Calculate percentage based on distance covered
    const progressPercentage = (currentStation.distance / totalDistance) * 100;
    return Math.min(Math.max(progressPercentage, 0), 100);
  };

  const trainPosition = calculateTrainPosition();

  const getStationStatusColor = (status) => {
    switch (status) {
      case "completed":
        return "text-success border-success bg-success/10";
      case "current":
        return "text-warning border-warning bg-warning/10";
      case "upcoming":
        return "text-muted-foreground border-muted bg-muted/10";
      default:
        return "text-muted-foreground border-muted";
    }
  };

  const getTimeStatusBadge = (status) => {
    switch (status) {
      case "completed":
        return (
          <Badge className="bg-success text-success-foreground text-xs">
            Completed
          </Badge>
        );
      case "current":
        return (
          <Badge className="bg-warning text-warning-foreground text-xs">
            Current
          </Badge>
        );
      case "upcoming":
        return (
          <Badge className="bg-muted text-muted-foreground text-xs">
            Upcoming
          </Badge>
        );
      default:
        return null;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between">
        <h4 className="font-semibold text-sm flex items-center gap-2">
          <Route className="h-4 w-4" />
          Route Progress: {train.startingStation} → {train.endingStation}
        </h4>
        <Badge variant="outline" className="text-xs">
          {train.estimatedDuration} journey
        </Badge>
      </div>

      <div className="bg-muted/20 rounded-lg p-4">
        {/* Train Position Indicator */}
        <div className="relative mb-6">
          <div className="flex items-center justify-between text-xs text-muted-foreground mb-2">
            <span>{routeStations[0].name}</span>
            <span className="font-medium text-warning">
              {trainPosition.toFixed(0)}% Complete
            </span>
            <span>{routeStations[routeStations.length - 1].name}</span>
          </div>

          {/* Railway line */}
          <div className="relative h-2 bg-muted rounded-full overflow-hidden">
            {/* Completed track */}
            <div
              className="absolute left-0 top-0 h-full bg-success transition-all duration-1000 ease-out"
              style={{ width: `${trainPosition}%` }}
            />

            {/* Train icon positioned on the track */}
            <div
              className="absolute top-1/2 transform -translate-y-1/2 -translate-x-1/2 transition-all duration-1000 ease-out"
              style={{ left: `${trainPosition}%` }}
            >
              <div className="relative">
                {/* Train icon with glow effect */}
                <div className="w-6 h-6 bg-warning rounded-full border-2 border-background shadow-lg flex items-center justify-center animate-pulse">
                  <Train className="h-3 w-3 text-warning-foreground" />
                </div>

                {/* Speed indicator */}
                <div className="absolute -top-8 left-1/2 transform -translate-x-1/2 bg-background border border-border rounded px-2 py-1 text-xs font-medium whitespace-nowrap shadow-sm">
                  {train.currentSpeed || "65"} km/h
                </div>
              </div>
            </div>
          </div>

          {/* Distance markers */}
          <div className="flex justify-between text-xs text-muted-foreground mt-1">
            <span>0 km</span>
            <span>
              {Math.round(routeStations[routeStations.length - 1].distance / 2)}{" "}
              km
            </span>
            <span>{routeStations[routeStations.length - 1].distance} km</span>
          </div>
        </div>

        <div className="space-y-3">
          {routeStations.map((station, index) => (
            <div key={station.code} className="relative">
              {/* Connection line */}
              {index < routeStations.length - 1 && (
                <div className="absolute left-6 top-12 w-0.5 h-8 bg-border"></div>
              )}

              <div
                className={cn(
                  "flex items-center gap-4 p-3 rounded-lg border transition-all",
                  station.status === "current"
                    ? "border-white animate-pulse-border"
                    : station.status === "completed"
                    ? "border-green-500"
                    : getStationStatusColor(station.status)
                )}
              >
                {/* Station indicator */}
                <div
                  className={cn(
                    "w-3 h-3 rounded-full border-2 flex-shrink-0",
                    station.status === "current"
                      ? "bg-warning border-green-500 animate-pulse"
                      : station.status === "completed"
                      ? "bg-background border-green-500"
                      : "bg-background border-muted"
                  )}
                >
                  {station.status === "current" && (
                    <div className="w-full h-full rounded-full bg-warning animate-ping"></div>
                  )}
                </div>

                <div className="flex-1 min-w-0">
                  <div className="flex items-center justify-between mb-1">
                    <div className="flex items-center gap-2">
                      <span className="font-medium text-sm">
                        {station.code}
                      </span>
                      <span className="text-xs text-muted-foreground">
                        ({station.platform})
                      </span>
                    </div>
                    {getTimeStatusBadge(station.status)}
                  </div>

                  <div className="text-sm text-muted-foreground mb-1">
                    {station.name}
                  </div>

                  <div className="flex items-center justify-between text-xs">
                    <div className="flex items-center gap-4">
                      {station.arrival !== "Start" && (
                        <span>Arr: {station.arrival}</span>
                      )}
                      {station.departure !== "End" && (
                        <span>Dep: {station.departure}</span>
                      )}
                    </div>
                    <span className="text-muted-foreground">
                      {station.distance} KMs
                    </span>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Journey Summary */}
      <div className="grid grid-cols-3 gap-4 p-3 bg-muted/10 rounded-lg text-center">
        <div>
          <div className="text-xs text-muted-foreground">Total Distance</div>
          <div className="font-semibold text-sm">849 KMs</div>
        </div>
        <div>
          <div className="text-xs text-muted-foreground">Progress</div>
          <div className="font-semibold text-sm text-warning">
            {trainPosition.toFixed(0)}%
          </div>
        </div>
        <div>
          <div className="text-xs text-muted-foreground">Avg Speed</div>
          <div className="font-semibold text-sm">
            {train.currentSpeed || "65"} km/h
          </div>
        </div>
      </div>
    </div>
  );
}

export function TrainCard({ train, onHalt, onLetGo }) {
  const [isExpanded, setIsExpanded] = useState(false);

  const getStatusColor = (status) => {
    switch (status) {
      case "on-time":
        return "bg-success text-success-foreground";
      case "delayed":
        return "bg-warning text-warning-foreground";
      case "halted":
        return "bg-destructive text-destructive-foreground";
      default:
        return "bg-muted text-muted-foreground";
    }
  };

  const getStatusIcon = (status) => {
    switch (status) {
      case "on-time":
        return <Play className="h-3 w-3" />;
      case "delayed":
        return <AlertTriangle className="h-3 w-3" />;
      case "halted":
        return <Pause className="h-3 w-3" />;
      default:
        return <Clock className="h-3 w-3" />;
    }
  };

  return (
    <Card className="transition-all duration-200 hover:shadow-md">
      <CardHeader
        className="cursor-pointer"
        onClick={() => setIsExpanded(!isExpanded)}
      >
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex flex-col">
              <CardTitle className="text-lg font-semibold">
                {train.name}
              </CardTitle>
              <div className="text-sm text-muted-foreground">
                ID: {train.id}
              </div>
            </div>
            <Badge className={cn("text-xs", getStatusColor(train.status))}>
              {getStatusIcon(train.status)}
              <span className="ml-1 capitalize">{train.status}</span>
            </Badge>
          </div>
          {isExpanded ? (
            <ChevronUp className="h-5 w-5 text-muted-foreground" />
          ) : (
            <ChevronDown className="h-5 w-5 text-muted-foreground" />
          )}
        </div>

        <div className="space-y-2">
          <div className="flex items-center gap-2 text-sm">
            <Route className="h-4 w-4 text-muted-foreground" />
            <span className="font-medium">{train.startingStation}</span>
            <span className="text-muted-foreground">→</span>
            <span className="font-medium">{train.endingStation}</span>
          </div>

          <div className="flex items-center gap-4 text-sm text-muted-foreground">
            <div className="flex items-center gap-1">
              <Clock className="h-3 w-3" />
              <span>Dep: {train.departureTime}</span>
            </div>
            <div className="flex items-center gap-1">
              <Timer className="h-3 w-3" />
              <span>Duration: {train.estimatedDuration}</span>
            </div>
          </div>
        </div>
      </CardHeader>

      {isExpanded && (
        <CardContent className="pt-0">
          <div className="space-y-6">
            <RouteVisualization train={train} />

            {/* Basic Train Information */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 p-4 bg-muted/30 rounded-lg">
              <div className="space-y-2">
                <h4 className="font-semibold text-sm flex items-center gap-2">
                  <Train className="h-4 w-4" />
                  Train Details
                </h4>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Train Number:</span>
                    <span className="font-medium">{train.number}</span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Type:</span>
                    <span className="font-medium">
                      {train.type || "Express"}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">Priority:</span>
                    <Badge variant="outline" className="text-xs">
                      {train.priority || "Normal"}
                    </Badge>
                  </div>
                </div>
              </div>

              <div className="space-y-2">
                <h4 className="font-semibold text-sm flex items-center gap-2">
                  <Clock className="h-4 w-4" />
                  Schedule Information
                </h4>
                <div className="space-y-1 text-sm">
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">
                      Scheduled Departure:
                    </span>
                    <span className="font-medium">
                      {train.scheduledDeparture || train.departureTime}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">
                      Estimated Arrival:
                    </span>
                    <span className="font-medium">
                      {train.estimatedArrival || train.eta}
                    </span>
                  </div>
                  <div className="flex justify-between">
                    <span className="text-muted-foreground">
                      Total Duration:
                    </span>
                    <span className="font-medium">
                      {train.estimatedDuration}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            {/* Current Status */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <MapPin className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">Current Station</div>
                    <div className="text-sm text-muted-foreground">
                      {train.currentStation}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Navigation className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">Current Location</div>
                    <div className="text-sm text-muted-foreground">
                      {train.location}
                    </div>
                  </div>
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex items-center gap-2">
                  <Clock className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">Next Station ETA</div>
                    <div className="text-sm text-muted-foreground">
                      {train.eta}
                    </div>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Timer className="h-4 w-4 text-muted-foreground" />
                  <div>
                    <div className="text-sm font-medium">Delay Status</div>
                    <div
                      className={cn(
                        "text-sm font-medium",
                        train.delay ? "text-warning" : "text-success"
                      )}
                    >
                      {train.delay ? `+${train.delay} min` : "On Time"}
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Additional Details */}
            {train.additionalInfo && (
              <div className="p-3 bg-muted/20 rounded-lg">
                <h4 className="font-semibold text-sm mb-2">
                  Additional Information
                </h4>
                <p className="text-sm text-muted-foreground">
                  {train.additionalInfo}
                </p>
              </div>
            )}

            {/* Control Actions */}
            <div className="flex gap-2 pt-4 border-t">
              <Button
                variant={train.status === "halted" ? "default" : "outline"}
                size="sm"
                onClick={() =>
                  train.status === "halted"
                    ? onLetGo(train.id)
                    : onHalt(train.id)
                }
                className="flex-1"
              >
                {train.status === "halted" ? (
                  <>
                    <Play className="h-4 w-4 mr-2" />
                    Let Go
                  </>
                ) : (
                  <>
                    <Pause className="h-4 w-4 mr-2" />
                    Halt
                  </>
                )}
              </Button>

              <Button
                variant="outline"
                size="sm"
                className="flex-1 bg-transparent"
              >
                <Navigation className="h-4 w-4 mr-2" />
                Track Route
              </Button>
            </div>
          </div>
        </CardContent>
      )}
    </Card>
  );
}
