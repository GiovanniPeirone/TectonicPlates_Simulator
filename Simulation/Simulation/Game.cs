using OpenTK.Windowing.Common;
using OpenTK.Windowing.Desktop;
using System;
using OpenTK.Graphics.OpenGL;
using OpenTK.Mathematics;

namespace Simulation
{
    public class Game : GameWindow
    {
        private int vertexBufferHandle;
        private int shaderProgramHandle;
        private int vertexArrayHandle;

        public Game() : base(GameWindowSettings.Default, NativeWindowSettings.Default)
        {
            this.CenterWindow(new Vector2i(1080, 720));
        }

        protected override void OnResize(ResizeEventArgs e)
        {
            GL.Viewport(0, 0, e.Width, e.Height);
            base.OnResize(e);
        }

        protected override void OnLoad()
        {
            Console.WriteLine("Ventana se Abre");
            GL.ClearColor(new Color4(0.3f, 0.4f, 0.5f, 1f));

            float[] vertices = new float[]
            {
                0.0f, 0.5f, 0,
                0.5f, -0.5f, 0,
                -0.5f, -0.5f, 0,
            };

            // Crear y configurar el VAO
            vertexArrayHandle = GL.GenVertexArray();
            GL.BindVertexArray(vertexArrayHandle);

            // Crear y configurar el VBO
            vertexBufferHandle = GL.GenBuffer();
            GL.BindBuffer(BufferTarget.ArrayBuffer, vertexBufferHandle);
            GL.BufferData(BufferTarget.ArrayBuffer, vertices.Length * sizeof(float), vertices, BufferUsageHint.StaticDraw);

            GL.VertexAttribPointer(0, 3, VertexAttribPointerType.Float, false, 3 * sizeof(float), 0);
            GL.EnableVertexAttribArray(0);

            // Desenlazar VBO y VAO
            GL.BindBuffer(BufferTarget.ArrayBuffer, 0);
            GL.BindVertexArray(0);

            // Shaders
            string vertexShaderCode = @"
                #version 330 core
                layout (location = 0) in vec3 aPosition;
                void main()
                {
                    gl_Position = vec4(aPosition, 1f);    
                }
            ";

            string pixelShaderCode = @"
                #version 330 core
                out vec4 outputColor;
                void main()
                {
                    outputColor = vec4(1.0, 1.0, 0.0, 1.0);
                }
            ";

            int vertexShaderHandle = GL.CreateShader(ShaderType.VertexShader);
            GL.ShaderSource(vertexShaderHandle, vertexShaderCode);
            GL.CompileShader(vertexShaderHandle);
            CheckShaderCompilation(vertexShaderHandle, "Vertex");

            int pixelShaderHandle = GL.CreateShader(ShaderType.FragmentShader);
            GL.ShaderSource(pixelShaderHandle, pixelShaderCode);
            GL.CompileShader(pixelShaderHandle);
            CheckShaderCompilation(pixelShaderHandle, "Fragment");

            // Crear y enlazar programa de shaders
            shaderProgramHandle = GL.CreateProgram();
            GL.AttachShader(shaderProgramHandle, vertexShaderHandle);
            GL.AttachShader(shaderProgramHandle, pixelShaderHandle);
            GL.LinkProgram(shaderProgramHandle);

            GL.GetProgram(shaderProgramHandle, GetProgramParameterName.LinkStatus, out int linkStatus);
            if (linkStatus == 0)
            {
                Console.WriteLine($"Error en el enlace del programa de shaders: {GL.GetProgramInfoLog(shaderProgramHandle)}");
            }

            GL.DetachShader(shaderProgramHandle, vertexShaderHandle);
            GL.DetachShader(shaderProgramHandle, pixelShaderHandle);
            GL.DeleteShader(vertexShaderHandle);
            GL.DeleteShader(pixelShaderHandle);

            base.OnLoad();
        }

        private void CheckShaderCompilation(int shaderHandle, string shaderType)
        {
            GL.GetShader(shaderHandle, ShaderParameter.CompileStatus, out int success);
            if (success == 0)
            {
                string infoLog = GL.GetShaderInfoLog(shaderHandle);
                Console.WriteLine($"Error en la compilación del {shaderType} shader: {infoLog}");
            }
        }

        protected override void OnUnload()
        {
            Console.WriteLine("Ventana se cierra");
            GL.BindBuffer(BufferTarget.ArrayBuffer, 0);
            GL.DeleteBuffer(vertexBufferHandle);

            GL.BindVertexArray(0);
            GL.DeleteVertexArray(vertexArrayHandle);

            GL.UseProgram(0);
            GL.DeleteProgram(shaderProgramHandle);

            base.OnUnload();
        }

        protected override void OnRenderFrame(FrameEventArgs args)
        {
            GL.Clear(ClearBufferMask.ColorBufferBit);

            GL.UseProgram(shaderProgramHandle);
            GL.BindVertexArray(vertexArrayHandle);
            GL.DrawArrays(PrimitiveType.Triangles, 0, 3);

            this.Context.SwapBuffers();
            base.OnRenderFrame(args);

            // Comprobar errores de OpenGL después de cada frame
            ErrorCode error = GL.GetError();
            if (error != ErrorCode.NoError)
            {
                Console.WriteLine($"Error de OpenGL: {error}");
            }
        }
    }
}