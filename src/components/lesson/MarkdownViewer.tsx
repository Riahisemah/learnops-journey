import { useState } from "react";
import { Copy, Check, BookOpen, Code, Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { Input } from "@/components/ui/input";
import { Badge } from "@/components/ui/badge";
import { cn } from "@/lib/utils";

interface ContentSection {
  title: string;
  content: string;
  codeBlocks?: { language: string; code: string }[];
}

interface MarkdownViewerProps {
  theory: ContentSection;
  practice: ContentSection;
}

const CodeBlock = ({ language, code }: { language: string; code: string }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="relative group rounded-lg overflow-hidden border border-border my-4">
      <div className="flex items-center justify-between px-4 py-2 bg-secondary border-b border-border">
        <Badge variant="outline" className="text-xs font-mono">{language}</Badge>
        <Button
          variant="ghost"
          size="sm"
          onClick={handleCopy}
          className="h-7 gap-1 text-xs"
        >
          {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
          {copied ? 'Copié !' : 'Copier'}
        </Button>
      </div>
      <pre className="p-4 overflow-x-auto bg-muted/50">
        <code className="text-sm font-mono text-foreground">{code}</code>
      </pre>
    </div>
  );
};

const RenderContent = ({ section, searchQuery }: { section: ContentSection; searchQuery: string }) => {
  const highlightText = (text: string) => {
    if (!searchQuery) return text;
    const regex = new RegExp(`(${searchQuery})`, 'gi');
    const parts = text.split(regex);
    return parts.map((part, i) => 
      regex.test(part) 
        ? <mark key={i} className="bg-warning/30 rounded px-0.5">{part}</mark> 
        : part
    );
  };

  return (
    <div className="prose-sm max-w-none space-y-4">
      <div className="text-foreground leading-relaxed whitespace-pre-line">
        {highlightText(section.content)}
      </div>
      {section.codeBlocks?.map((block, i) => (
        <CodeBlock key={i} language={block.language} code={block.code} />
      ))}
    </div>
  );
};

const MarkdownViewer = ({ theory, practice }: MarkdownViewerProps) => {
  const [searchQuery, setSearchQuery] = useState('');

  return (
    <div className="space-y-4">
      {/* Search */}
      <div className="relative">
        <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
        <Input
          placeholder="Rechercher dans la documentation..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          className="pl-10"
        />
      </div>

      {/* Tabbed Content */}
      <Tabs defaultValue="theory" className="w-full">
        <TabsList className="grid w-full grid-cols-2">
          <TabsTrigger value="theory" className="gap-2">
            <BookOpen className="h-4 w-4" />
            Théorie
          </TabsTrigger>
          <TabsTrigger value="practice" className="gap-2">
            <Code className="h-4 w-4" />
            Pratique
          </TabsTrigger>
        </TabsList>

        <TabsContent value="theory">
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-bold mb-4">{theory.title}</h2>
              <RenderContent section={theory} searchQuery={searchQuery} />
            </CardContent>
          </Card>
        </TabsContent>

        <TabsContent value="practice">
          <Card>
            <CardContent className="p-6">
              <h2 className="text-xl font-bold mb-4">{practice.title}</h2>
              <RenderContent section={practice} searchQuery={searchQuery} />
            </CardContent>
          </Card>
        </TabsContent>
      </Tabs>
    </div>
  );
};

export default MarkdownViewer;
