import 'package:cached_network_image/cached_network_image.dart';
import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class ImageWithBackgroundResultView extends StatelessWidget {
  final ItemModel model;
  const ImageWithBackgroundResultView({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text(model.title)),
      body: AppBody(
        builder: (windowWidth, windowHeight, windowSize) {
          return GridView.builder(
            gridDelegate: SliverGridDelegateWithMaxCrossAxisExtent(
                maxCrossAxisExtent: 200),
            itemBuilder: (context, index) {
              return ClipRRect(
                borderRadius: BorderRadius.circular(AppValues.kRadius),
                child: CachedNetworkImage(
                  imageUrl: model.url,
                  fit: BoxFit.cover,
                ),
              );
            },
          );
        },
      ),
    );
  }
}
