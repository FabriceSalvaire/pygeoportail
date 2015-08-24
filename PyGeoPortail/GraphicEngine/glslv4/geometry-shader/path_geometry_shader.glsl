/* *********************************************************************************************** */

// #shader_type geometry

#version 330
#extension GL_EXT_geometry_shader4 : enable

/* *********************************************************************************************** */

#include(../include/model_view_projection_matrix.glsl)

#include(../include/vector.glsl)

/* *********************************************************************************************** */

uniform float line_width = 5;
uniform float antialias_diameter = 1;

uniform float z_value = 0;

uniform vec2 scale = vec2(1);
uniform vec2 translation = vec2(0);
uniform float rotation = 0;

/* *********************************************************************************************** */

layout(lines_adjacency) in;
layout(triangle_strip, max_vertices=4) out;

/* *********************************************************************************************** */

in VertexAttributesIn
{
  vec2 position;
  vec4 colour;
} vertexIn[];

/* *********************************************************************************************** */

out VertexAttributes
{
  vec2 uv;
  float line_length;
  float line_width;
  vec4 colour;
  float cap;
} vertex;

/* *********************************************************************************************** */

void
compute_offsets(in vec2 dir1, in vec2 dir2, in float w,
		out vec2 offset, out float u_offset)
{
  float angle = angle_between(dir1, dir2) / 2;
  // bissector
  vec2 n = normalize(normal(dir1 + dir2));
  offset = w / cos(angle) * n;
  u_offset = w * tan(angle);
}

/* *********************************************************************************************** */

void
emit_vertex(in vec2 position, in vec2 uv, in float cap)
{
  vertex.cap = cap;
  vertex.uv = uv;
  position *= scale;
  position = rotate(position, rotation);
  position += translation;
  gl_Position =  model_view_projection_matrix * vec4(position, z_value, 1);
  EmitVertex();
}

/* *********************************************************************************************** */

void main()
{
  vertex.colour = vertexIn[0].colour;

  // If color is fully transparent we just will discard the fragment later
  /* if (vertex.colour.a <= .0) */
  /*   return; */
  
  vec2 pos0 = vertexIn[0].position;
  vec2 pos1 = vertexIn[1].position;
  vec2 pos2 = vertexIn[2].position;
  vec2 pos3 = vertexIn[3].position;

  float line_length = distance(pos1, pos2);
  vertex.line_length = line_length;
  
  // Thickness below 1 pixel are represented using a 1 pixel thickness
  // and a modified alpha
  vertex.colour.a = min(line_width, vertex.colour.a);
  vertex.line_width = max(line_width, 1);

  // This is the actual half width of the line
  float w = ceil(1.25*antialias_diameter + line_width) / 2;

  vec2 dir0 = direction(pos0, pos1);
  
  vec2 dir1 = direction(pos1, pos2);
  vec2 normal1 = normal(dir1);
  vec2 tangential_offset1 = dir1 * w;
  vec2 normal_offset1 = normal1 * w;

  vec2 dir2 = direction(pos2, pos3);

  float cap1 = 0;
  if (pos0 == pos1) {
    cap1 = -1;
    pos1 -= tangential_offset1;

    emit_vertex(pos1 - normal_offset1, vec2(-w, -w), cap1);
    emit_vertex(pos1 + normal_offset1, vec2(-w, w), cap1);
  } else {
    vec2 o1;
    float u1;
    compute_offsets(dir0, dir1, w, o1, u1);
    
    emit_vertex(pos1 - o1, vec2(-u1, -w), cap1);
    emit_vertex(pos1 + o1, vec2(u1, w), cap1);
  }

  float cap2 = 0;
  if (pos2 == pos3) {
    cap2 = 1;
    pos2 += tangential_offset1;
    float u = line_length + w;

    emit_vertex(pos2 - normal_offset1, vec2(u, -w), cap2);
    emit_vertex(pos2 + normal_offset1, vec2(u, w), cap2);
  } else {
    vec2 o2;
    float u2;
    compute_offsets(dir1, dir2, w, o2, u2);

    emit_vertex(pos2 - o2, vec2(line_length + u2, -w), cap2);
    emit_vertex(pos2 + o2, vec2(line_length - u2,  w), cap2);
  }
  
  EndPrimitive();
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
