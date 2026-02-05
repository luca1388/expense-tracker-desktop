from datetime import date
import tkinter as tk
from tkinter import ttk

from services.analysis_service import AnalysisService


class AnalysisTab(ttk.Frame):
    def __init__(self, master, analysis_service: AnalysisService):
        super().__init__(master)

        self.analysis_service = analysis_service
        self.label = ttk.Label(self, text="Analisi spese")
        self.label.pack(pady=20)

    def refresh(self, start_date: date, end_date: date):
        result = self.analysis_service.get_expense_summary(start_date, end_date)
        # rendering in step successivo
        print(result.overall)
