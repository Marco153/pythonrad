import imgui
from PIL import Image
from imgui.integrations.glfw import GlfwRenderer
import glfw
from OpenGL.GL import *

# Initialize GLFW for window creation
if not glfw.init():
    print("Could not initialize GLFW")
    exit(1)

width = 800
height = 600
window = glfw.create_window(width, height, "PyImGui Example", None, None)
if not window:
    glfw.terminate()
    print("Could not create window")
    exit(1)

# Make the OpenGL context current
glfw.make_context_current(window)

# Set up Dear ImGui context
imgui.create_context()
impl = GlfwRenderer(window)

# Application state variables
show_demo_window = True
text_input_value = ""
senha_value = ""
checkbox_state = False

def create_texture(image_path):
    # Load the image using PIL (Pillow)
    image = Image.open(image_path)
    #image = image.transpose(Image.FLIP_TOP_BOTTOM)  # Flip the image for OpenGL's coordinate system
    img_data = image.convert("RGBA").tobytes()  # Convert image to RGBA and get the byte data
    width, height = image.size

    # Generate a texture ID
    texture_id = glGenTextures(1)

    # Bind the texture to apply subsequent settings
    glBindTexture(GL_TEXTURE_2D, texture_id)

    # Define the texture parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)  # Minification filter
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)  # Magnification filter
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)  # Wrap mode for S axis
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE)  # Wrap mode for T axis

    # Upload the texture data to OpenGL
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    # Generate mipmaps (optional for better texture quality when scaling down)
    glGenerateMipmap(GL_TEXTURE_2D)

    # Unbind the texture to avoid unintentional modifications
    glBindTexture(GL_TEXTURE_2D, 0)

    return texture_id	


logo = create_texture("logo.jpg")

style = imgui.get_style()
style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.1, 0.5, 0.8, 1.0) 
page = 0

def AlunoPanel():
	imgui.text("Aluno")
def ProfessorPanel():
	with imgui.begin_table("table", 5):
		imgui.table_next_row()
		imgui.table_next_column()
		imgui.text("Nome")

		imgui.table_next_column()
		imgui.text("Java")

		imgui.table_next_column()
		imgui.text('Progamação web')
		imgui.table_next_row()
		imgui.table_next_column()

		imgui.text("João")
		nota_1 = 0 
		nota_2 = 0 
		imgui.table_next_column()
		imgui.input_int("##nota1", nota_1)
		imgui.table_next_column()
		imgui.input_int("##nota2", nota_2)

def Login():
	global text_input_value
	global senha_value
	global page

	window_width, window_height = imgui.get_window_size()

	image_width = 100
	image_height = 100
    # Calculate the position to center the image
	x_pos = (window_width - image_width) / 2.0
	y_pos = (window_height - image_height) / 2.0
	imgui.set_cursor_pos_x(x_pos)
	#imgui.set_cursor_pos_y(y_pos)

	imgui.image(logo, image_width, image_height, border_color=(0, 0, 0, 1))

	imgui.text("matricula")
	changed, text_input_value = imgui.input_text("##matricula", text_input_value, 256)
    # Text input field
	imgui.text("senha")
	#senha_input = ""
	changed, senha_value = imgui.input_text("##senha", senha_value, 256, flags=imgui.INPUT_TEXT_PASSWORD)

    # Button example
	if imgui.button("entrar"):
		if text_input_value == "aluno" and senha_value == "1234":
			page = 1
		elif text_input_value == "professor" and senha_value == "1234":
			page = 2

io = imgui.get_io()

new_font = io.fonts.add_font_from_file_ttf(
    "arial.ttf", 20,
)
impl.refresh_font_texture()
# Main application loop
while not glfw.window_should_close(window):
	glfw.poll_events()
	impl.process_inputs()

    # Start a new ImGui fram
	imgui.new_frame()

	imgui.set_next_window_position(0, 0)
	imgui.set_next_window_size(width, height)

    # Create a new fullscreen window
	imgui.begin("Fullscreen UI Window", flags=imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | imgui.WINDOW_NO_COLLAPSE)

	imgui.push_font(new_font)
	if page == 0:
		Login()
	elif page == 1:
		AlunoPanel()
	elif page == 2:
		ProfessorPanel()
	imgui.pop_font()

    # End the UI window
	imgui.end()

    # OpenGL rendering
	glClearColor(0.1, 0.1, 0.1, 1)
	glClear(GL_COLOR_BUFFER_BIT)

    # Render the ImGui frame
	imgui.render()
	impl.render(imgui.get_draw_data())

    # Swap buffers
	glfw.swap_buffers(window)

# Cleanup
impl.shutdown()
glfw.terminate()
