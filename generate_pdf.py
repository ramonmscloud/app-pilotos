from fpdf import FPDF
import sys

# Ensure utf-8 output for console just in case
sys.stdout.reconfigure(encoding='utf-8')

class PDF(FPDF):
    def header(self):
        # Logo could go here
        self.set_font('Helvetica', 'B', 16)
        # Title
        self.cell(0, 10, 'Normas de Seguridad y Operaciones', align='C')
        self.ln(20)

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        # Page number
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', align='C')

    def chapter_title(self, num, label):
        self.set_font('Helvetica', 'B', 12)
        self.set_fill_color(230, 230, 230)  # Light gray
        self.cell(0, 8, f'{num}. {label}', fill=True, ln=True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 11)
        self.multi_cell(0, 6, body)
        self.ln(5)

# Create PDF instance
pdf = PDF()
pdf.alias_nb_pages()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

# Define the content with corrected text (Spanish accents handled via Latin-1 encoding implicitly by FPDF2 with core fonts hopefully, 
# but best to ensure strings are clean). 
# FPDF2 handles unicode if we use a font that supports it. 
# With core fonts (Helvetica), it tries to map to Latin-1. 
# We need to make sure our strings are regular Python strings.

content_data = [
    {
        "title": "Gestión Administrativa y Requisitos del Personal",
        "items": [
            ("Acreditación y Registro", 
             "Ninguna operación puede iniciarse sin que el piloto cuente con su registro de operador de UAS (el cual debe estar reseñado en el aeromodelo), su licencia de la Federación de Deportes Aéreos correspondiente y un seguro de responsabilidad civil (mínimo 750.000 DEG)."),
            ("Estado del Piloto", 
             "Está estrictamente prohibido operar bajo los efectos del alcohol o sustancias psicoactivas, o en condiciones de fatiga, enfermedad o medicación que mermen las capacidades."),
            ("Supervisión Operativa", 
             "El control de la actividad en el campo recae en el Responsable de Operaciones de Vuelo (o en su defecto, el primer piloto validado socio que llegue al club), quien debe supervisar que todos apliquen el Manual de Operaciones y posean sus certificados vigentes.")
        ]
    },
    {
        "title": "Control Pre-vuelo y Planificación de Seguridad",
        "items": [
            ("Responsabilidad del Piloto", 
             "El piloto es el único y máximo responsable de cada vuelo que realice, asumiendo íntegramente el cumplimiento de la normativa vigente y los reglamentos internos del CRA. El piloto deberá cumplir todas las normas y protocolos establecidos en el Manual de Operaciones (MO), además de los reglamentos del CRA."),
            ("Verificación del Espacio Aéreo", 
             "Es obligatorio consultar ENAIRE DRONES antes de cada jornada (para <300m) o antes de cada operación (para <500m), seleccionando la opción de altura +120m para verificar NOTAMs activos."),
            ("Evaluación del Entorno", 
             "El piloto debe confirmar que la meteorología es apta y que la zona de operaciones está despejada de personas no participantes, manteniendo siempre un margen de riesgo en tierra según la regla 1:1 respecto a la altura."),
            ("Inspección Técnica Obligatoria", 
             "Se debe verificar el ensamblaje, el movimiento de mandos, el enlace de radio y, especialmente, la configuración activa del sistema Fail-Safe y altímetros.")
        ]
    },
    {
        "title": "Normas durante la Operación y Vigilancia",
        "items": [
            ("Binomio Piloto-Observador", 
             "No se permite el vuelo sin la presencia de un observador registrado encargado de la vigilancia continuada del espacio aéreo para detectar otros tráficos o peligros."),
            ("Prioridad y No-Conflicto", 
             "Ante la presencia de una aeronave tripulada, se debe aterrizar de inmediato o bajar la cota de vuelo siguiendo el esquema de no conflicto."),
            ("Protocolos de Comunicación", 
             "Es obligatorio comunicar de viva voz a los presentes las maniobras de acceso a pista, despegue, aproximación y aterrizaje, así como cualquier situación de emergencia."),
            ("Límites de Seguridad", 
             "Las operaciones deben mantenerse siempre en VLOS (alcance visual), sin superar una energía cinética de 34 KJ y respetando los límites de la \"caja de maniobras\" (Ver delimitación Zona de Vuelo del CRA en la app).")
        ]
    },
    {
        "title": "Gestión de Contingencias y Emergencias",
        "items": [
            ("Fallo de Control", 
             "En caso de pérdida de enlace, el sistema Fail-Safe debe actuar. Como última medida ante un fallo permanente, se debe intentar minimizar la energía de impacto parando el motor."),
            ("Intervención del Responsable", 
             "El Responsable de Operaciones tiene la potestad de inmovilizar aeromodelos inseguros o pilotos con mala salud."),
            ("Notificación de Sucesos", 
             "Todo incidente grave o accidente debe comunicarse de inmediato al Director de Operaciones y, si hay lesiones o daños a terceros, se debe llamar al 112 y tramitar el reporte oficial ante AESA.")
        ]
    },
    {
        "title": "Control Post-vuelo y Disciplina",
        "items": [
            ("Inspección Final", 
             "Tras el aterrizaje, se debe realizar una inspección técnica para detectar daños o fatiga en los componentes."),
            ("Registros", 
             "El piloto debe dejar constancia de los datos del vuelo y el estado del UAS, completando informes de sucesos si fuera necesario."),
            ("Régimen Disciplinario", 
             "Cualquier incumplimiento de estas normas fusionadas de seguridad y operación será sancionado conforme a los Estatutos del Club, que deben estar siempre a disposición de la autoridad.")
        ]
    }
]

# Build PDF content
for index, section in enumerate(content_data):
    pdf.chapter_title(index + 1, section["title"])
    
    for item_title, item_text in section["items"]:
        # Bold item title
        pdf.set_font('Helvetica', 'B', 11)
        pdf.write(6, f"- {item_title}: ")
        
        # Regular text
        pdf.set_font('Helvetica', '', 11)
        pdf.multi_cell(0, 6, item_text)
        pdf.ln(2) # Little gap between items
    
    pdf.ln(5) # Gap between sections

# Output
output_path = "Normas_Seguridad_y_Operaciones_Limpias.pdf"
pdf.output(output_path)
print(f"PDF generado: {output_path}")
