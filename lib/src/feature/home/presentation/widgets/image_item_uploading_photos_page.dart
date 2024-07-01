// ignore_for_file: public_member_api_docs, sort_constructors_first

import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class ImageItemUploadingPhotosPage extends StatelessWidget {
  final File imageFile;

  const ImageItemUploadingPhotosPage({
    super.key,
    required this.imageFile,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      alignment: Alignment.topRight,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(8.r),
        image: DecorationImage(
          image: FileImage(imageFile),
          fit: BoxFit.cover,
        ),
      ),
      child: GestureDetector(
        // onTap: ,
        child: Container(
          margin: EdgeInsets.all(5.r),
          decoration: BoxDecoration(
            color: Colors.grey[700],
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
