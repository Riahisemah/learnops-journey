import { useState } from "react";
import { Play, Clock, CheckCircle2, List } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AspectRatio } from "@/components/ui/aspect-ratio";
import { cn } from "@/lib/utils";
import { VideoData } from "@/data/video-data";

interface VideoPlayerProps {
  video: VideoData;
  completed: boolean;
  onMarkWatched: () => void;
}

const formatTime = (seconds: number): string => {
  const m = Math.floor(seconds / 60);
  const s = seconds % 60;
  return `${m}:${s.toString().padStart(2, '0')}`;
};

const VideoPlayer = ({ video, completed, onMarkWatched }: VideoPlayerProps) => {
  const [showChapters, setShowChapters] = useState(false);

  return (
    <div className="space-y-4">
      {/* Video Embed */}
      <Card className="overflow-hidden">
        <AspectRatio ratio={16 / 9}>
          {video.embedUrl ? (
            <iframe
              src={video.embedUrl}
              title={video.title}
              className="w-full h-full"
              allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
              allowFullScreen
            />
          ) : (
            <div className="w-full h-full bg-secondary flex items-center justify-center">
              <div className="text-center">
                <Play className="h-16 w-16 mx-auto text-muted-foreground mb-2" />
                <p className="text-muted-foreground">Vidéo à venir</p>
              </div>
            </div>
          )}
        </AspectRatio>
      </Card>

      {/* Controls */}
      <div className="flex items-center justify-between gap-4 flex-wrap">
        <div className="flex items-center gap-2">
          <Button
            variant="outline"
            size="sm"
            className="gap-2"
            onClick={() => setShowChapters(!showChapters)}
          >
            <List className="h-4 w-4" />
            Chapitres ({video.chapters.length})
          </Button>
        </div>

        <Button
          variant={completed ? "outline" : "default"}
          size="sm"
          onClick={onMarkWatched}
          className={cn(
            "gap-2",
            !completed && "bg-accent hover:bg-accent/90 text-accent-foreground"
          )}
        >
          <CheckCircle2 className="h-4 w-4" />
          {completed ? "Vu ✓" : "Marquer comme vu"}
        </Button>
      </div>

      {/* Chapters */}
      {showChapters && (
        <Card>
          <CardContent className="p-4">
            <h3 className="font-semibold mb-3 flex items-center gap-2">
              <List className="h-4 w-4" />
              Chapitres
            </h3>
            <div className="space-y-2">
              {video.chapters.map((chapter, index) => (
                <div
                  key={index}
                  className="flex items-center gap-3 p-2 rounded-lg hover:bg-secondary transition-colors cursor-pointer"
                >
                  <Badge variant="secondary" className="font-mono text-xs min-w-[50px] justify-center">
                    <Clock className="h-3 w-3 mr-1" />
                    {formatTime(chapter.time)}
                  </Badge>
                  <span className="text-sm">{chapter.title}</span>
                </div>
              ))}
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  );
};

export default VideoPlayer;
