#version 150

#moj_import <fog.glsl>

in vec3 Position;
in vec4 Color;
in vec2 UV0;
in ivec2 UV2;

uniform sampler2D Sampler0;
uniform sampler2D Sampler2;
uniform float GameTime;

uniform mat4 ModelViewMat;
uniform mat4 ProjMat;
uniform mat3 IViewRotMat;
uniform int FogShape;
uniform vec2 ScreenSize;

out float vertexDistance;
out vec4 vertexColor;
out vec2 texCoord0;

flat out int p;

float get_hp_fully(float r, float g) {
    if (r <= 255.0 && g == 255.0) return 0.5 * (2.0 - (r / g));
    if (r == 255.0 && g <= 255.0) return 0.5 * (g / 255.0);
    return 0.5;
}

void main() {
    gl_Position = ProjMat * ModelViewMat * vec4(Position, 1);
    vertexColor = Color * texelFetch(Sampler2, UV2 / 16, 0);

    vertexDistance = length((ModelViewMat * vec4(Position, 1)).xyz);
    texCoord0 = UV0;

    const vec2[4] corners = vec2[4](vec2(0), vec2(0, 1), vec2(1), vec2(1, 0));
    vec2 coord = corners[gl_VertexID % 4];

    float alpha = round(texture(Sampler0, UV0).a * 255);

    p = 0;
    if (alpha == 251 && Position.z > 0)
    {   
        p = 1;
        gl_Position.xy = vec2(coord * 2 - 1) * vec2(1, -1);
        gl_Position.zw = vec2(-1, 1);
        vertexColor = Color;
    }
    vec3 rgb = vec3(floor(Color.r * 255), floor(Color.g * 255), floor(Color.b * 255));
    if (rgb.b == 2)
    {
	float fully = Color.r;
        float tick = 4.0 + fully * 10.0;
        float a = mod((GameTime * 20000), tick * 2) / tick;
	if (a > 1) a = 1 - (a - 1);
	vertexColor = vec4(1.0, fully - 0.08, fully - 0.08, 1.0);
	vertexColor *= 0.85 + (0.15 * (fully * 2 - a));
        vertexColor.a = 0.05 + gl_Position.w / 14.0;
	if (vertexColor.a > 0.6) vertexColor.a = 0.6;
    }
}
