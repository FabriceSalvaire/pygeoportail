/* *********************************************************************************************** */

// #shader_type geometry

/* *********************************************************************************************** */

#version 330
#extension GL_EXT_geometry_shader4 : enable

/* *********************************************************************************************** */

#include(../include/model_view_projection_matrix.glsl)

#include(../include/vector.glsl)

/* *********************************************************************************************** */
	      
uniform float line_width = 5;
uniform float antialias_diameter = 1;

uniform vec2 scale = vec2(1);
uniform vec2 translation = vec2(0);
uniform float rotation = 0;

/* *********************************************************************************************** */

layout(lines) in; // P.inf -> P.sup
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
  float line_width;
  vec4 colour;
} vertex;

/* *********************************************************************************************** */

void emit_vertex(in vec2 position, in vec2 uv)
{
  vertex.uv = uv;
  position *= scale;
  position = rotate(position, rotation);
  position += translation;
  gl_Position =  model_view_projection_matrix * vec4(position, 0, 1);
  EmitVertex();
}

/* *********************************************************************************************** */

void main()
{
  vertex.colour = vertexIn[0].colour;

  /*
   *  tl--*--tr
   *  |       |
   *  *   +   *
   *  |       |
   *  bl--*--br
   *
   */

  vec2 pos_bl = vertexIn[0].position;
  vec2 pos_tr = vertexIn[1].position;
  vec2 pos_tl = vec2(pos_bl.x, pos_tr.y);
  vec2 pos_br = vec2(pos_tr.x, pos_bl.y);
  
  emit_vertex(pos_bl, vec2(-1, -1));
  emit_vertex(pos_tl, vec2(-1,  1));
  emit_vertex(pos_br, vec2( 1, -1));
  emit_vertex(pos_tr, vec2( 1,  1));
  EndPrimitive();
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
