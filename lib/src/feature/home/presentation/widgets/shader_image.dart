import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';

class ImageWithShader extends StatelessWidget {
  final String url;
  final List<Color>? colors;
  const ImageWithShader({
    super.key,
    required this.url,
    this.colors,
  });

  @override
  Widget build(BuildContext context) {
    return ShaderMask(
        blendMode: BlendMode.srcATop,
        shaderCallback: (Rect bounds) {
          return LinearGradient(
            colors: colors ??
                [
                  Colors.black,
                  Colors.black87,
                  Colors.black54,
                  Colors.black38,
                  Colors.black12,
                  Colors.white12,
                  // Colors.transparent
                ],
            begin: Alignment.bottomCenter,
            end: Alignment.topCenter,
          ).createShader(bounds);
        },
        child: CachedNetworkImage(
          imageUrl: url,
          fit: BoxFit.cover,
        ));
  }
}
