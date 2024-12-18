import tkinter as tk
from tkinter import ttk
from typing import Optional, Dict
import platform

class ScrollHandler:
    """
    Gestisce lo scrolling del canvas con supporto per multiple pagine/tab.
    """
    # Dizionario statico per tenere traccia di tutti i canvas attivi
    _active_canvases: Dict[str, 'ScrollHandler'] = {}
    
    def __init__(self, canvas: tk.Canvas, content_frame: ttk.Frame, window: tk.Toplevel):
        self.canvas = canvas
        self.content_frame = content_frame
        self.window = window
        self.is_windows = platform.system() == "Windows"
        self.scroll_sensitivity = 2
        
        # Registra questo handler nel dizionario usando l'id del canvas
        self._active_canvases[str(self.canvas)] = self
        
        self.setup_scroll_bindings()
        self.setup_canvas()

    def setup_canvas(self) -> None:
        """Configura il canvas per lo scrolling"""
        self.canvas.configure(
            scrollregion=self.canvas.bbox("all"),
            yscrollincrement=20,
            highlightthickness=0
        )

    def setup_scroll_bindings(self) -> None:
        """Configura i binding per lo scrolling"""
        # Binding per il ridimensionamento
        self.content_frame.bind("<Configure>", self.configure_scroll)
        
        # Binding per il mouse sul canvas specifico
        self.canvas.bind("<Enter>", self.on_enter_canvas)
        self.canvas.bind("<Leave>", self.on_leave_canvas)
        
        # Binding globali se non esistono già
        if self.is_windows and not hasattr(self.window, '_scroll_bound'):
            self.window.bind_all("<MouseWheel>", self._dispatch_scroll_windows)
            self.window.bind("<Destroy>", self.on_destroy, add="+")
            self.window._scroll_bound = True
        elif not self.is_windows and not hasattr(self.window, '_scroll_bound'):
            self.window.bind_all("<Button-4>", self._dispatch_scroll_unix)
            self.window.bind_all("<Button-5>", self._dispatch_scroll_unix)
            self.window.bind("<Destroy>", self.on_destroy, add="+")
            self.window._scroll_bound = True

    def configure_scroll(self, event: Optional[tk.Event] = None) -> None:
        """Aggiorna la regione di scrolling del canvas"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _dispatch_scroll_windows(self, event: tk.Event) -> None:
        """Dispatcha l'evento di scroll al canvas corretto in Windows"""
        widget = self.window.winfo_containing(event.x_root, event.y_root)
        if widget:
            # Trova il canvas parent più vicino
            current = widget
            while current and not isinstance(current, tk.Canvas):
                current = current.master
            
            if current and str(current) in self._active_canvases:
                handler = self._active_canvases[str(current)]
                handler._perform_scroll(-1 * (event.delta // 120))

    def _dispatch_scroll_unix(self, event: tk.Event) -> None:
        """Dispatcha l'evento di scroll al canvas corretto in Unix"""
        widget = self.window.winfo_containing(event.x_root, event.y_root)
        if widget:
            # Trova il canvas parent più vicino
            current = widget
            while current and not isinstance(current, tk.Canvas):
                current = current.master
            
            if current and str(current) in self._active_canvases:
                handler = self._active_canvases[str(current)]
                delta = -1 if event.num == 4 else 1
                handler._perform_scroll(delta)

    def _perform_scroll(self, delta: float) -> None:
        """Esegue lo scrolling"""
        try:
            current_pos = self.canvas.yview()
            new_pos = current_pos[0] + (delta * 0.01 * self.scroll_sensitivity)
            new_pos = max(0.0, min(1.0, new_pos))
            
            if new_pos != current_pos[0]:
                self.canvas.yview_moveto(new_pos)
        except Exception:
            self.canvas.yview_scroll(int(delta), "units")

    def on_enter_canvas(self, event: Optional[tk.Event] = None) -> None:
        """Attiva quando il mouse entra nel canvas"""
        if event and event.widget:
            event.widget.focus_set()

    def on_leave_canvas(self, event: Optional[tk.Event] = None) -> None:
        """Disattiva quando il mouse esce dal canvas"""
        if self.window:
            self.window.focus_set()

    def on_destroy(self, event: Optional[tk.Event] = None) -> None:
        """Pulisce i binding quando la finestra viene chiusa"""
        if event and event.widget == self.window:
            try:
                # Rimuovi questo handler dal dizionario
                if str(self.canvas) in self._active_canvases:
                    del self._active_canvases[str(self.canvas)]
                
                # Se non ci sono più handler attivi, rimuovi i binding globali
                if not self._active_canvases:
                    if self.is_windows:
                        self.window.unbind_all("<MouseWheel>")
                    else:
                        self.window.unbind_all("<Button-4>")
                        self.window.unbind_all("<Button-5>")
                    if hasattr(self.window, '_scroll_bound'):
                        delattr(self.window, '_scroll_bound')
                
                self.content_frame.unbind("<Configure>")
                self.canvas.unbind("<Enter>")
                self.canvas.unbind("<Leave>")
            except tk.TclError:
                pass