#version 330

in vec2 uv;
uniform sampler2D fonttex;
uniform vec4 foreground;
uniform vec4 background;

// render color
out vec4 out_color;

void main() {
	out_color = mix(background, foreground, texture(fonttex, uv).r);
}
