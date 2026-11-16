import tkinter as tk
from tkinter import ttk
import arabic_reshaper
from bidi.algorithm import get_display

class DISCProfiler(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("تقييم الشخصية DISC")
        self.geometry("900x750")
        self.configure(bg="#f5f7fa")
        
        self.style = ttk.Style()
        self.style.configure("TFrame", background="#f5f7fa")
        self.style.configure("TButton", font=("Arial", 12), padding=10)
        self.style.configure("TLabel", background="#f5f7fa", font=("Arial", 12))
        self.style.configure("Title.TLabel", background="#f5f7fa", font=("Arial", 20, "bold"))
        self.style.configure("Question.TLabel", background="#f5f7fa", font=("Arial", 14))
        
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        self.current_page = 0
        self.user_answers = []
        self.disc_scores = {"D": 0, "I": 0, "S": 0, "C": 0}
        
        self.pages = [
            self.create_welcome_page,
            self.create_question_page_1,
            self.create_question_page_2,
            self.create_question_page_3,
            self.create_question_page_4,
            self.create_question_page_5,
            self.create_question_page_6,
            self.create_question_page_7,
            self.create_question_page_8,
            self.create_question_page_9,
            self.create_question_page_10,
            self.create_results_page
        ]
        
        self.questions = [
            {
                "text": "عند مواجهة تحدي، عادة ما:",
                "options": [
                    ("أتولى القيادة وأتخذ قرارات سريعة", "D"),
                    ("أقنع الآخرين بالانضمام إلى نهجي", "I"),
                    ("أعمل بطريقة منهجية للوصول إلى حل مستقر", "S"),
                    ("أحلل جميع التفاصيل قبل اتخاذ القرار", "C")
                ]
            },
            {
                "text": "في بيئة الفريق، أفضل أن:",
                "options": [
                    ("أقود الفريق وأحدد الاتجاه", "D"),
                    ("أحفز الفريق وأحافظ على الروح المعنوية", "I"),
                    ("أدعم أعضاء الفريق وأحافظ على الانسجام", "S"),
                    ("أتأكد من أن كل شيء يتبع الإجراءات الصحيحة", "C")
                ]
            },
            {
                "text": "عند التواصل، أميل إلى أن أكون:",
                "options": [
                    ("مباشر وواضح", "D"),
                    ("معبر ومتحمس", "I"),
                    ("هادئ ودبلوماسي", "S"),
                    ("دقيق ومفصل", "C")
                ]
            },
            {
                "text": "تحت الضغط، من المحتمل أن:",
                "options": [
                    ("أتولى السيطرة وأمضي قدماً", "D"),
                    ("أبقى متفائلاً وأُلهم الآخرين", "I"),
                    ("أبقى صبوراً وداعماً", "S"),
                    ("أركز على إنجاز الأمور بدقة", "C")
                ]
            },
            {
                "text": "أعظم نقاط قوتي في العمل هي:",
                "options": [
                    ("تحقيق النتائج والتغلب على العقبات", "D"),
                    ("بناء العلاقات والتأثير على الآخرين", "I"),
                    ("الموثوقية وخلق الاستقرار", "S"),
                    ("ضمان الجودة والدقة", "C")
                ]
            },
            {
                "text": "أسلوبي في اتخاذ القرارات عادة ما يكون:",
                "options": [
                    ("سريع وحاسم", "D"),
                    ("بديهي وموجه نحو الناس", "I"),
                    ("حذر ومراعي", "S"),
                    ("منهجي ومعتمد على الحقائق", "C")
                ]
            },
            {
                "text": "ما يحفزني أكثر في العمل هو:",
                "options": [
                    ("تحقيق الأهداف والفوز", "D"),
                    ("التقدير والتفاعل الاجتماعي", "I"),
                    ("الاستقرار ومساعدة الآخرين", "S"),
                    ("العمل الجيد وإنجاز الأمور بشكل صحيح", "C")
                ]
            },
            {
                "text": "في حالات الصراع، أميل إلى:",
                "options": [
                    ("مواجهة المشاكل مباشرة", "D"),
                    ("التعبير عن المشاعر والبحث عن حل وسط", "I"),
                    ("السعي للانسجام وتجنب المواجهة", "S"),
                    ("التركيز على الحقائق واتباع البروتوكولات", "C")
                ]
            },
            {
                "text": "سرعة عملي المفضلة هي:",
                "options": [
                    ("سريع ومركز على النتائج", "D"),
                    ("ديناميكي ومتنوع", "I"),
                    ("ثابت ومتسق", "S"),
                    ("منهجي وشامل", "C")
                ]
            },
            {
                "text": "أكبر مخاوفي في بيئة العمل هو:",
                "options": [
                    ("فقدان السيطرة أو استغلالي", "D"),
                    ("التجاهل أو الرفض", "I"),
                    ("التغييرات المفاجئة أو عدم الاستقرار", "S"),
                    ("الخطأ أو انتقادي لضعف الجودة", "C")
                ]
            }
        ]
        
        self.show_current_page()
    
    def format_arabic(self, text):
        """Format Arabic text for proper display"""
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    
    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
    
    def show_current_page(self):
        self.clear_frame()
        self.pages[self.current_page]()
    
    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_current_page()
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_current_page()
    
    def record_answer(self, question_idx, answer_type):
        if question_idx < len(self.user_answers):
            # Update existing answer
            old_answer = self.user_answers[question_idx]
            self.disc_scores[old_answer] -= 1
            self.user_answers[question_idx] = answer_type
        else:
            self.user_answers.append(answer_type)
        
        self.disc_scores[answer_type] += 1
        self.next_page()
    
    def create_welcome_page(self):
        # Decorative header
        header_frame = tk.Frame(self.main_frame, bg="#4A90E2", height=120)
        header_frame.pack(fill="x", pady=(0, 30))
        header_frame.pack_propagate(False)
        
        title_text = self.format_arabic("مرحباً بك في تقييم الشخصية DISC")
        title_label = tk.Label(
            header_frame,
            text=title_text,
            font=("Arial", 24, "bold"),
            bg="#4A90E2",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Content frame
        content_frame = tk.Frame(self.main_frame, bg="white", relief="solid", borderwidth=1)
        content_frame.pack(fill="both", expand=True, padx=20, pady=10)
        
        desc_text = """
هذا التقييم سيساعد على تحديد ميولك السلوكية بناءً على نموذج DISC:

D - الهيمنة: كيف تستجيب للتحديات
I - التأثير: كيف تتفاعل وتؤثر على الآخرين
S - الثبات: سرعتك واتساقك
C - الامتثال: كيف تستجيب للقواعد والإجراءات

ستجيب على 10 أسئلة حول تفضيلاتك وسلوكياتك.
لا توجد إجابات صحيحة أو خاطئة - فقط اختر ما يصفك بشكل أفضل.
        """
        
        formatted_desc = self.format_arabic(desc_text.strip())
        
        description = tk.Label(
            content_frame,
            text=formatted_desc,
            wraplength=700,
            justify="right",
            font=("Arial", 13),
            bg="white",
            fg="#2c3e50",
            padx=30,
            pady=30
        )
        description.pack(fill="both", expand=True)
        
        # Start button
        start_text = self.format_arabic("ابدأ التقييم")
        start_button = tk.Button(
            self.main_frame,
            text=start_text,
            font=("Arial", 16, "bold"),
            bg="#4CAF50",
            fg="white",
            padx=60,
            pady=15,
            cursor="hand2",
            relief="flat",
            command=self.next_page
        )
        start_button.pack(pady=30)
    
    def create_question_template(self, question_idx):
        # Progress indicator
        progress_frame = tk.Frame(self.main_frame, bg="#f5f7fa")
        progress_frame.pack(pady=(10, 20))
        
        progress_text = self.format_arabic(f"10 من {question_idx + 1} سؤال")
        progress_label = tk.Label(
            progress_frame,
            text=progress_text,
            font=("Arial", 12),
            bg="#f5f7fa",
            fg="#7f8c8d"
        )
        progress_label.pack()
        
        # Progress bar with dots
        dots_frame = tk.Frame(self.main_frame, bg="#f5f7fa")
        dots_frame.pack(pady=(0, 30))
        
        for i in range(10):
            color = "#4CAF50" if i < question_idx else "#e0e0e0"
            if i == question_idx:
                color = "#2196F3"
            dot = tk.Label(dots_frame, text="●", font=("Arial", 16), 
                          fg=color, bg="#f5f7fa")
            dot.pack(side="right", padx=3)
        
        # Question card
        question_card = tk.Frame(self.main_frame, bg="white", relief="solid", 
                                borderwidth=1, padx=30, pady=30)
        question_card.pack(fill="both", expand=True, padx=20)
        
        question = self.questions[question_idx]
        question_text = self.format_arabic(question["text"])
        
        question_label = tk.Label(
            question_card,
            text=question_text,
            font=("Arial", 18, "bold"),
            bg="white",
            fg="#2c3e50",
            wraplength=700,
            justify="right"
        )
        question_label.pack(pady=(0, 30), anchor="e")
        
        # Options
        for i, (option_text, option_type) in enumerate(question["options"]):
            formatted_option = self.format_arabic(option_text)
            
            option_frame = tk.Frame(question_card, bg="white")
            option_frame.pack(fill="x", pady=8)
            
            option_button = tk.Button(
                option_frame,
                text=formatted_option,
                font=("Arial", 13),
                bg="#ecf0f1",
                fg="#2c3e50",
                padx=20,
                pady=15,
                cursor="hand2",
                relief="flat",
                anchor="e",
                command=lambda qt=option_type: self.record_answer(question_idx, qt)
            )
            option_button.pack(fill="x", padx=10)
            
            # Hover effect
            option_button.bind("<Enter>", lambda e, btn=option_button: btn.config(bg="#3498db", fg="white"))
            option_button.bind("<Leave>", lambda e, btn=option_button: btn.config(bg="#ecf0f1", fg="#2c3e50"))
        
        # Navigation
        nav_frame = tk.Frame(self.main_frame, bg="#f5f7fa")
        nav_frame.pack(pady=20)
        
        if question_idx > 0:
            back_text = self.format_arabic("رجوع")
            back_button = tk.Button(
                nav_frame,
                text=back_text,
                font=("Arial", 12, "bold"),
                bg="#95a5a6",
                fg="white",
                padx=30,
                pady=10,
                cursor="hand2",
                relief="flat",
                command=self.prev_page
            )
            back_button.pack(side="right", padx=10)
    
    def create_question_page_1(self):
        self.create_question_template(0)
    
    def create_question_page_2(self):
        self.create_question_template(1)
    
    def create_question_page_3(self):
        self.create_question_template(2)
    
    def create_question_page_4(self):
        self.create_question_template(3)
    
    def create_question_page_5(self):
        self.create_question_template(4)
    
    def create_question_page_6(self):
        self.create_question_template(5)
    
    def create_question_page_7(self):
        self.create_question_template(6)
    
    def create_question_page_8(self):
        self.create_question_template(7)
    
    def create_question_page_9(self):
        self.create_question_template(8)
    
    def create_question_page_10(self):
        self.create_question_template(9)
    
    def create_bar_chart(self, parent):
        """Create a bar chart using tkinter Canvas"""
        chart_frame = tk.Frame(parent, bg="white", relief="solid", borderwidth=2)
        chart_frame.pack(pady=20)
        
        canvas = tk.Canvas(chart_frame, width=700, height=400, bg="white")
        canvas.pack(padx=20, pady=20)
        
        # Chart data
        categories = ['الهيمنة', 'التأثير', 'الثبات', 'الامتثال']
        categories_en = ['D', 'I', 'S', 'C']
        values = [self.disc_scores["D"], self.disc_scores["I"], 
                  self.disc_scores["S"], self.disc_scores["C"]]
        colors = ['#FF5733', '#33FF57', '#3357FF', '#FFD700']
        
        # Chart dimensions
        bar_width = 100
        max_height = 250
        margin_left = 100
        margin_right = 100
        spacing = 130
        
        # Title
        title_text = self.format_arabic("ملفك الشخصي DISC")
        canvas.create_text(350, 30, text=title_text, 
                          font=("Arial", 18, "bold"))
        
        # Draw bars from right to left
        total_width = len(categories) * spacing
        start_x = 600
        
        for i, (category, category_en, value, color) in enumerate(zip(categories, categories_en, values, colors)):
            x = start_x - (i * spacing)
            bar_height = (value / 10) * max_height
            y = 320 - bar_height
            
            # Draw bar with shadow
            canvas.create_rectangle(x + 3, y + 3, x + bar_width + 3, 320 + 3, 
                                   fill="#cccccc", outline="")
            canvas.create_rectangle(x, y, x + bar_width, 320, 
                                   fill=color, outline="black", width=2)
            
            # Draw value on top
            canvas.create_text(x + bar_width/2, y - 15, 
                             text=str(value), font=("Arial", 16, "bold"))
            
            # Draw Arabic label
            formatted_cat = self.format_arabic(category)
            canvas.create_text(x + bar_width/2, 345, 
                             text=formatted_cat, font=("Arial", 12, "bold"))
            
            # Draw English label
            canvas.create_text(x + bar_width/2, 365, 
                             text=f"({category_en})", font=("Arial", 10))
        
        # Draw Y-axis
        canvas.create_line(margin_left - 20, 70, margin_left - 20, 320, width=2)
        
        # Y-axis labels
        for i in range(0, 11, 2):
            y = 320 - (i / 10) * max_height
            canvas.create_text(margin_left - 45, y, text=str(i), font=("Arial", 11))
            canvas.create_line(margin_left - 25, y, margin_left - 20, y, width=1)
    
    def create_results_page(self):
        # Header
        header_frame = tk.Frame(self.main_frame, bg="#4A90E2", height=100)
        header_frame.pack(fill="x", pady=(0, 20))
        header_frame.pack_propagate(False)
        
        title_text = self.format_arabic("نتائج ملفك الشخصي DISC")
        title_label = tk.Label(
            header_frame,
            text=title_text,
            font=("Arial", 22, "bold"),
            bg="#4A90E2",
            fg="white"
        )
        title_label.pack(expand=True)
        
        # Create the chart
        self.create_bar_chart(self.main_frame)
        
        # Get dominant profile
        categories = ['الهيمنة', 'التأثير', 'الثبات', 'الامتثال']
        categories_en = ['D', 'I', 'S', 'C']
        values = [self.disc_scores["D"], self.disc_scores["I"], 
                  self.disc_scores["S"], self.disc_scores["C"]]
        
        max_score = max(values)
        dominant_indices = [i for i, v in enumerate(values) if v == max_score]
        dominant_types = [categories[i] for i in dominant_indices]
        
        if len(dominant_types) > 1:
            dominant_text = f"سماتك المهيمنة هي: {' و '.join(dominant_types)}"
        else:
            dominant_text = f"سمتك المهيمنة هي: {dominant_types[0]}"
        
        formatted_dominant = self.format_arabic(dominant_text)
        
        dominant_label = tk.Label(
            self.main_frame,
            text=formatted_dominant,
            font=("Arial", 16, "bold"),
            bg="#f5f7fa",
            fg="#2c3e50"
        )
        dominant_label.pack(pady=15)
        
        # Profile description
        descriptions = {
            "D": "شخصيات الهيمنة مباشرة وحاسمة وحلالة للمشاكل. يركزون على النتائج ويقبلون التحديات ويتخذون إجراءات.",
            "I": "المؤثرون متفائلون واجتماعيون ومتحدثون. يستمتعون ببناء العلاقات وهم متواصلون مقنعون.",
            "S": "الشخصيات الثابتة صبورة ومخلصة وداعمة. يقدرون الاستقرار والاتساق والبيئات المتناغمة.",
            "C": "الشخصيات الممتثلة تحليلية ومهتمة بالتفاصيل ومنهجية. يركزون على الدقة والجودة والأساليب المنطقية."
        }
        
        primary_idx = values.index(max(values))
        primary_type = categories_en[primary_idx]
        primary_category = categories[primary_idx]
        
        description_text = f"السمة الأساسية - {primary_category}:\n{descriptions[primary_type]}"
        formatted_description = self.format_arabic(description_text)
        
        desc_frame = tk.Frame(self.main_frame, bg="white", relief="solid", borderwidth=1)
        desc_frame.pack(fill="x", padx=40, pady=15)
        
        description_label = tk.Label(
            desc_frame,
            text=formatted_description,
            wraplength=700,
            justify="right",
            font=("Arial", 13),
            bg="white",
            fg="#34495e",
            padx=30,
            pady=20
        )
        description_label.pack()
        
        # Restart button
        restart_text = self.format_arabic("إعادة التقييم")
        restart_button = tk.Button(
            self.main_frame,
            text=restart_text,
            font=("Arial", 14, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=40,
            pady=12,
            cursor="hand2",
            relief="flat",
            command=self.restart_assessment
        )
        restart_button.pack(pady=20)
    
    def restart_assessment(self):
        self.current_page = 0
        self.user_answers = []
        self.disc_scores = {"D": 0, "I": 0, "S": 0, "C": 0}
        self.show_current_page()

if __name__ == "__main__":
    app = DISCProfiler()
    app.mainloop()