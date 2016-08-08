/// the "main" function / application code is all manually authored.
/// The generated renderer is called like a regular function.

#include <GLFW/glfw3.h>
#include <RSL/runtime.h>
#include "vrender.h" // the generated rsl code

const unsigned int resWidth = 1440;
const unsigned int resHeight = 900;

#define EXIT_FAILURE -1
#define EXIT_SUCCESS 0

static void error_callback(int error, const char* description)
{
    std::cerr<< "Error: " << description<< std::endl;
}

static void key_callback(GLFWwindow* window, int key, int scancode, int action, int mods)
{
    if (key == GLFW_KEY_ESCAPE && action == GLFW_PRESS)
        glfwSetWindowShouldClose(window, GLFW_TRUE);
}

int main(void)
{
    GLFWwindow* window;

    glfwSetErrorCallback(error_callback);

    if (!glfwInit())
        exit(EXIT_FAILURE);

    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, vrender::GL::major); // rsl backend compiled against specific gl featureset
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, vrender::GL::minor);

    window = glfwCreateWindow(resWidth, resHeight, "Hello RSL", NULL, NULL);

    if (!window)
    {
        glfwTerminate();
        exit(EXIT_FAILURE);
    }

    glfwSetKeyCallback(window, key_callback);
    glfwMakeContextCurrent(window);

    glfwSwapInterval(1);

    rsl::Image2D<vengine::Pixel> framebuffer(resWidth, resHeight);

    while (!glfwWindowShouldClose(window))
    {
        // func HelloRSL (Image2D<Pixel> renderTargetIn) ->(Image2D<Pixel> renderTargetOut)
        // if the module returns more than one argument, the compiler generates type HelloRSL_Return as a struct.
        // if there's one return argument, it should just be the expected return type
        framebuffer = renderReturn = vengine::HelloRSL(framebuffer);

        ///image needs to be compatible with presentable format.  (eg, less than 4 elements)
        ///we have the minor inefficiency here that RSL will be headless, then we have a built in screen quad or copy pixels
        ///pass to actually put the pixes on the display.
        rsl::display_image(framebuffer);

        glfwSwapBuffers(window);
        glfwPollEvents();
    }

    glfwDestroyWindow(window);
    glfwTerminate();
    
    exit(EXIT_SUCCESS);
}
