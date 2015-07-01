/* *********************************************************************************************** */

// #shader_type geometry

/* *********************************************************************************************** */

#version 330
#extension GL_EXT_geometry_shader4 : enable

/* *********************************************************************************************** */

#include(../include/model_view_projection_matrix.glsl)

/* *********************************************************************************************** */

uniform bool unscale_margin = false; // Fixme: name
uniform float margin = 0; // to add a margin on the ROI
uniform float grip_margin = 20; // px
uniform bool paint_grips = true; // false;
uniform bool paint_inner_box = false;

/* *********************************************************************************************** */

layout(lines) in; // P.inf -> P.sup
layout(line_strip, max_vertices=18) out; // 2*5 + 4*2 vertices = 18

/* *********************************************************************************************** */

in VertexAttributesIn
{
  vec2 position;
  vec4 colour;
} vertexIn[];

/* *********************************************************************************************** */

out VertexAttributes
{
  vec4 colour;
} vertex;

/* *********************************************************************************************** */

void emit_vertex(vec2 position)
{
  gl_Position = model_view_projection_matrix * vec4(position, 0, 1);
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

  if (paint_inner_box)
    {
      // Paint inner box: (5 vertices, 4 segments)
      vec2 pos_bl = vertexIn[0].position;
      vec2 pos_tr = vertexIn[1].position;
      vec2 pos_tl = vec2(pos_bl.x, pos_tr.y);
      vec2 pos_br = vec2(pos_tr.x, pos_bl.y);

      emit_vertex(pos_bl);
      emit_vertex(pos_tl);
      emit_vertex(pos_tr);
      emit_vertex(pos_br);
      emit_vertex(pos_bl);
      EndPrimitive();
    }

  // Enlarge box for margin
  float scaled_margin = margin; // Fixme: recompute grip
  if (unscale_margin)
    scaled_margin *= viewport_scale;
  vec2 pos_bl = vertexIn[0].position - vec2(scaled_margin);
  vec2 pos_tr = vertexIn[1].position + vec2(scaled_margin);

  vec2 scaled_grip_margin = vec2(0);
  if (paint_grips)
    {
      // Enlarge box for grip margin
      scaled_grip_margin = grip_margin * viewport_scale; // Fixme: recompute grip
      pos_bl -= vec2(scaled_grip_margin);
      pos_tr += vec2(scaled_grip_margin);
    }

  vec2 pos_tl = vec2(pos_bl.x, pos_tr.y);
  vec2 pos_br = vec2(pos_tr.x, pos_bl.y);

  // Paint outer box: (5 vertices, 4 segments)
  emit_vertex(pos_bl);
  emit_vertex(pos_tl);
  emit_vertex(pos_tr);
  emit_vertex(pos_br);
  emit_vertex(pos_bl);
  EndPrimitive();

  // Paint grip lines: (8 vertices, 4 segments)
  if (paint_grips)
    {
      vec2 offset;

      offset = vec2(scaled_grip_margin.x, 0);
      // tl - bl
      emit_vertex(pos_bl + offset);
      emit_vertex(pos_tl + offset);
      EndPrimitive();
      // tr - br
      emit_vertex(pos_tr - offset);
      emit_vertex(pos_br - offset);
      EndPrimitive();

      offset = vec2(0, scaled_grip_margin.y);
      // tl - tr
      emit_vertex(pos_tl - offset);
      emit_vertex(pos_tr - offset);
      EndPrimitive();
      // bl - br
      emit_vertex(pos_bl + offset);
      emit_vertex(pos_br + offset);
      EndPrimitive();
    }
}

/* *********************************************************************************************** *
 *
 * End
 *
 * *********************************************************************************************** */
