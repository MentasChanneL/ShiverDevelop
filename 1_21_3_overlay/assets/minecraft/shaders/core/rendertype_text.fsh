#version 150

#moj_import <minecraft:fog.glsl>

uniform sampler2D Sampler0;

uniform vec4 ColorModulator;
uniform float FogStart;
uniform float FogEnd;
uniform vec4 FogColor;
uniform float GameTime;

uniform vec2 ScreenSize;

in float vertexDistance;
in vec4 vertexColor;
in vec2 texCoord0;

flat in int p;

out vec4 fragColor;

#moj_import <effect_utils.glsl>

void main() {
    vec4 color = texture(Sampler0, texCoord0) * vertexColor * ColorModulator;

    if (p == 1)
    {
        color = vec4(0, 0, 0, 1);
        vec2 centerUV = gl_FragCoord.xy / ScreenSize - 0.5;
        
        if (abs(centerUV.y) * 2 < 1 - mix(vertexColor.r, vertexColor.b, vertexColor.a))
        {
            color = vec4(0);
        }
    }

    if (color.a == 0) {
        discard;
    }

    fragColor = linear_fog(color, vertexDistance, FogStart, FogEnd, FogColor);
}
