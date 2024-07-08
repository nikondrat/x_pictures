import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';

class ImageWithShader extends StatelessWidget {
  final String url;
  const ImageWithShader({super.key, required this.url});

  @override
  Widget build(BuildContext context) {
    return ShaderMask(
        blendMode: BlendMode.srcATop,
        shaderCallback: (Rect bounds) {
          return const LinearGradient(
            colors: [Colors.black, Colors.white12, Colors.transparent],
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
