// See https://aka.ms/new-console-template for more information
using OpenTK.Mathematics;
using OpenTK.Windowing.Common;
using OpenTK.Windowing.Desktop;
using Simulation;


var nativeWindowSettings = new NativeWindowSettings()
{
    ClientSize = new Vector2i(800, 600),
    Title = "LearnOpenTK - Creating a Window",
    // This is needed to run on macos
    Flags = ContextFlags.ForwardCompatible,
};

using (var window = new Window(GameWindowSettings.Default, nativeWindowSettings))
{
    window.Run();
}


