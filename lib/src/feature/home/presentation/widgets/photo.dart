import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class PhotoWidget extends StatelessWidget {
  final bool isBadPhoto;
  final String path;
  const PhotoWidget({
    super.key,
    this.isBadPhoto = true,
    required this.path,
  });

  @override
  Widget build(BuildContext context) {
    final color = isBadPhoto ? Colors.red : AppColors.greenColor;

    return SizedBox(
      width: 84,
      child: DecoratedBox(
        decoration: BoxDecoration(
          borderRadius: BorderRadius.circular(8),
          border: Border.all(color: color),
          image: DecorationImage(image: AssetImage(path), fit: BoxFit.cover),
        ),
        child: Align(
            alignment: Alignment.bottomRight,
            child: Padding(
              padding: const EdgeInsets.only(right: 8, bottom: 8),
              child: DecoratedBox(
                decoration: BoxDecoration(
                  shape: BoxShape.circle,
                  color: color.withAlpha(180),
                ),
                child: const Padding(
                  padding: EdgeInsets.all(2),
                  child: Icon(
                    Icons.done,
                    size: 10,
                  ),
                ),
              ),
            )),
      ),
    );
  }
}
