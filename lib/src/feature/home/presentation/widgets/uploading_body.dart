import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

import 'image_item_uploading_photos_page.dart';

class UploadingPhotosBody extends StatelessWidget {
  const UploadingPhotosBody({super.key});

  @override
  Widget build(BuildContext context) {
    final LoraStore loraStore = Provider.of<LoraStore>(context);
    final picker = ImagePicker();

    return SliverPadding(
      padding: EdgeInsets.only(left: 15.w, right: 15.w, bottom: 80.h),
      sliver: Observer(
          builder: (context) => SliverGrid(
                delegate: SliverChildBuilderDelegate(
                  (context, index) {
                    if (index < loraStore.photosLength) {
                      return ImageItemUploadingPhotosPage(
                          haveError: index == 3,
                          imageFile: loraStore.photos[index]);
                    }
                    if (index == loraStore.photosLength) {
                      return GestureDetector(
                        onTap: () async {
                          final pickedFiles = await picker.pickMultiImage();

                          if (pickedFiles.isNotEmpty) {
                            loraStore.addPhotos(pickedFiles);
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
                    }
                    return const SizedBox.shrink();
                  },
                  childCount: loraStore.photosLength < 9
                      ? loraStore.photosLength + 1
                      : 9,
                ),
                gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
                  crossAxisCount: 3,
                  childAspectRatio: .99,
                  mainAxisSpacing: 10,
                  crossAxisSpacing: 10,
                ),
              )),
    );
  }
}
