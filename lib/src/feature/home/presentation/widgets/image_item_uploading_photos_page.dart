// ignore_for_file: public_member_api_docs, sort_constructors_first

import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class ImageItemUploadingPhotosPage extends StatelessWidget {
  final XFile imageFile;
  final bool haveError;

  const ImageItemUploadingPhotosPage({
    super.key,
    required this.imageFile,
    this.haveError = false,
  });

  @override
  Widget build(BuildContext context) {
    final LoraStore loraStore = Provider.of<LoraStore>(context);

    return Container(
      alignment: Alignment.topRight,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(8.r),
        border: haveError ? Border.all(color: Colors.red) : null,
        image: DecorationImage(
          image: FileImage(File(imageFile.path)),
          fit: BoxFit.cover,
        ),
      ),
      foregroundDecoration: haveError
          ? BoxDecoration(
              color: Colors.red.withAlpha(100),
              borderRadius: BorderRadius.circular(8.r))
          : null,
      child: GestureDetector(
        onTap: () => loraStore.removePhoto(imageFile),
        child: Container(
          margin: EdgeInsets.all(5.r),
          padding: EdgeInsets.all(1.r),
          decoration: BoxDecoration(
            color: haveError ? Colors.red : Colors.grey[700],
            borderRadius: BorderRadius.circular(90.r),
          ),
          child: const Icon(
            Icons.close,
            color: Colors.white,
            size: 15,
          ),
        ),
      ),
    );
  }
}
