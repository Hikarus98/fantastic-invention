"""Lightweight ARIA desktop chat UI using only Python's Tkinter."""
from __future__ import annotations
import threading
import tkinter as tk
from tkinter import ttk

from .config import Config
from .llm import OllamaClient
from .router import route_command

class ARIAWindow:
    def __init__(self, root: tk.Tk):
        self.root=root
        self.root.title("ARIA | Local AI")
        self.root.geometry("760x620")
        self.root.minsize(560,420)
        self.root.configure(bg="#10151f")
        self.client=OllamaClient(Config())
        self._build()
        self._append("ARIA", "Hello! I'm ARIA. Ask me something or try: open Firefox, find ChatGPT, visit example.com.")

    def _build(self):
        style=ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("TButton",padding=8)
        header=tk.Frame(self.root,bg="#10151f",padx=18,pady=14); header.pack(fill="x")
        tk.Label(header,text="ARIA",font=("Segoe UI",22,"bold"),fg="#70e1ff",bg="#10151f").pack(side="left")
        self.status=tk.Label(header,text="● Local assistant",font=("Segoe UI",10),fg="#9ba8bb",bg="#10151f")
        self.status.pack(side="right")
        self.chat=tk.Text(self.root,wrap="word",state="disabled",bg="#171e2b",fg="#e7edf7",
                          insertbackground="white",font=("Segoe UI",11),relief="flat",padx=14,pady=12)
        self.chat.pack(fill="both",expand=True,padx=16,pady=(0,12))
        self.chat.tag_configure("who",foreground="#70e1ff",font=("Segoe UI",10,"bold"))
        bottom=tk.Frame(self.root,bg="#10151f",padx=16,pady=12); bottom.pack(fill="x")
        self.entry=tk.Entry(bottom,bg="#202938",fg="#ffffff",insertbackground="white",
                           font=("Segoe UI",11),relief="flat")
        self.entry.pack(side="left",fill="x",expand=True,ipady=10,padx=(0,8))
        self.entry.bind("<Return>",lambda _e:self.send())
        ttk.Button(bottom,text="Send",command=self.send).pack(side="right")
        self.entry.focus_set()

    def _append(self,who,message):
        self.chat.configure(state="normal")
        self.chat.insert("end",who+"\n","who")
        self.chat.insert("end",message+"\n\n")
        self.chat.see("end"); self.chat.configure(state="disabled")

    def send(self):
        text=self.entry.get().strip()
        if not text:return
        self.entry.delete(0,"end"); self._append("You",text)
        self.status.configure(text="● Working…",fg="#ffd166")
        threading.Thread(target=self._process,args=(text,),daemon=True).start()

    def _process(self,text):
        try:
            result=route_command(text)
            answer=result.message if result.handled else self.client.chat(text)
        except Exception as exc:
            answer=f"Error: {exc}"
        self.root.after(0,lambda:self._finish(answer))

    def _finish(self,answer):
        self._append("ARIA",answer)
        self.status.configure(text="● Ready",fg="#9ba8bb")

def main():
    root=tk.Tk()
    ARIAWindow(root)
    root.mainloop()

if __name__=="__main__": main()
