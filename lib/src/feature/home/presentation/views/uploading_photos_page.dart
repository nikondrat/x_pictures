import 'dart:io';

import 'package:flutter/material.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:image_picker/image_picker.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';
import 'package:x_pictures/src/feature/home/presentation/widgets/image_item_uploading_photos_page.dart';

class UploadingPhotosPage extends StatefulWidget {
  const UploadingPhotosPage({super.key});

  @override
  State<UploadingPhotosPage> createState() => _UploadingPhotosPageState();
}

class _UploadingPhotosPageState extends State<UploadingPhotosPage> {
  final picker = ImagePicker();
  List<File> imageFiles = [];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: const CustomAppBar(textName: 'Uploading photos'),
      floatingActionButton:
          CustomFloatingButton(buttonName: 'Continue', onTap: () => router.goNamed(AppViews.genderView)),
      body: CustomScrollView(
        slivers: <Widget>[
          SliverToBoxAdapter(
            child: Padding(
              padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 15.h),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    'Step 2 of 3',
                    style: AppStyles.subTitleTextStyle.copyWith(
                      fontSize: 10.sp,
                    ),
                  ),
                  SizedBox(
                    height: 5.h,
                  ),
                  Padding(
                    padding: EdgeInsets.only(right: 50.w),
                    child: Text(
                      'Your photos have been processed',
                      style: AppStyles.head1TextStyle,
                    ),
                  ),
                  SizedBox(
                    height: 5.h,
                  ),
                  Text(
                    'Description',
                    style: AppStyles.subTitleTextStyle.copyWith(
                      fontSize: 17.sp,
                    ),
                  ),
                  SizedBox(
                    height: 20.h,
                  ),
                  Text(
                    'Your photos',
                    style: AppStyles.title2TextStyle,
                  ),
                ],
              ),
            ),
          ),
          SliverPadding(
            padding: EdgeInsets.only(left: 15.w, right: 15.w, bottom: 80.h),
            sliver: SliverGrid(
              delegate: SliverChildBuilderDelegate(
                (context, index) {
                  return uploadPhoto(index, context);
                },
                childCount: imageFiles.length + 1,
              ),
              gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                crossAxisCount: 3,
                childAspectRatio: .99,
                mainAxisSpacing: 10,
                crossAxisSpacing: 10,
              ),
            ),
          )
        ],
      ),
    );
  }

  Widget uploadPhoto(int index, BuildContext context) {
    if (index < imageFiles.length) {
      return ImageItemUploadingPhotosPage(imageFile: imageFiles[index]);
    } else if (index == imageFiles.length) {
      return GestureDetector(
        onTap: () async {
          if (imageFiles.length < 12) {
            final pickedFile =
                await picker.pickImage(source: ImageSource.gallery);
            if (pickedFile != null) {
              setState(() {
                imageFiles.add(File(pickedFile.path));
              });
            }
          } else {
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(
                content: Text('Maximum of 12 photos can be uploaded.'),
              ),
            );
          }
        },
        child: Container(
          alignment: Alignment.center,
          decoration: BoxDecoration(
            color: const Color(0xff0D1120),
            borderRadius: BorderRadius.circular(8.r),
          ),
          child: const Icon(
            Icons.add,
            color: Colors.white,
            size: 32,
          ),
        ),
      );
    } else {
      return const SizedBox.shrink();
    }
  }
}
