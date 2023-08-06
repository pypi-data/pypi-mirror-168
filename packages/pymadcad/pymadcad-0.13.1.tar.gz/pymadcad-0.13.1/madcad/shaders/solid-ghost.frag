/*
	shader for solid objects, with diffuse aspect based on the angle to the camera and a skybox reflect
*/
#version 330

in vec3 sight;		// vector from object to eye
in vec3 normal;		// normal to the surface
flat in int flags;
uniform vec4 min_color;		// color for background
uniform vec4 max_color;		// color for edges
uniform vec3 select_color;	// color for selected border

// render color
out vec4 color;

void main() {
	vec3 nsight = normalize(sight);
	vec3 nnormal = normalize(normal);
	float front = dot(nnormal, nsight);
// 	float side = clamp(10*length(vec2(dFdx(front), dFdy(front))), 0, 1);
// 	float side = min(1, 1 / max(0, dot(nsight,nnormal) - 0.1));
	float side;
	if (dot(nsight, nnormal) < 0)	side = 0;
	else							side = min(0.7, pow(1 - dot(nsight, nnormal), 3));
// 	else							side = clamp(0, 0.7, 0.15 / dot(nsight, nnormal) - 0.2);
	
	if ((flags & 1) != 0)	color = mix(vec4(select_color,0), vec4(select_color,1), min(1,side+0.05));
	else					color = mix(min_color, max_color, side);
}


