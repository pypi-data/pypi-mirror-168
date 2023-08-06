#version 330

#define HALO		0x1
#define SCALED		0x2
#define CLIPED		0x4
#define SELECTED	0x8
#define HOVERED		0x16

uniform mat4 world;
uniform mat4 view;
uniform mat4 proj;
uniform vec4 selection;
uniform float hover;

in vec3 v_origin;
in vec3 v_local;
in vec3 v_normal;
in vec3 v_color;
in int flags;

out vec3 normal;
out vec3 color;

int main() 
{
	if (flags & SELECTED)	color = selection;
	else					color = v_color;
	
	vec4 position = view * world * vec4(v_origin,1);	// origin point
	float persp = dot(transpose(proj)[3], position);	// perspective factor for compensation
	
	// apply local position
	if (flags & (HALO|SCALED)) {
		vec3 local = v_local;
		// rotate if not halo
		if (flags & HALO == 0)	local = vec3(view * world * vec4(local,1));
		// compensate perspective if scaled
		if (flags & SCALED)		local *= persp;
		// add to origin
		position += vec4(local,0);
	}
	if (flags & HALO)	normal = v_normal;
	else				normal = mat3(view) * mat3(world) * v_normal;
	
	position = proj * position;
	position[2] += persp * prevail;
	gl_Position = position;
}
