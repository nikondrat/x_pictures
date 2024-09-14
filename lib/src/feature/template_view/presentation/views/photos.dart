import 'dart:io';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:mobx/mobx.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/core/constant/styles.dart';
import 'package:x_pictures/src/data.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';

class PhotosView extends StatelessWidget {
  final String? title;
  final List<MediaModel> models;
  final bool isProfile;
  const PhotosView(
      {super.key, this.title, required this.models, this.isProfile = false});

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;

    /*24 is for notification bar on Android*/
    final double itemHeight = (size.height - kToolbarHeight - 24) / 2.5;
    final double itemWidth = size.width / 2;

    final bool isAndroid = Platform.isAndroid;

    return Provider(
      create: (context) => MediaBodyStore(homeStore: context.read()),
      builder: (context, child) {
        final store = Provider.of<MediaBodyStore>(context);

        store.items = ObservableList.of(models);

        return Observer(builder: (context) {
          return Scaffold(
            appBar: AppBar(
              leadingWidth: store.isHasSelectedItems && !isAndroid ? 90 : null,
              leading: store.isHasSelectedItems
                  ? isAndroid
                      ? IconButton(
                          onPressed: () {
                            store.markAllNotSelected();
                          },
                          icon: const Icon(Icons.close))
                      : TextButton(
                          onPressed: () {
                            store.markAllSelected();
                          },
                          child: AutoSizeText(
                            t.common.select_all,
                            style: textTheme.bodySmall!,
                          ),
                        )
                  : CustomBackButton(
                      onTap: () {
                        router.goNamed(AppViews.homePageRoute);
                      },
                    ),
              title: Text(
                store.isHasSelectedItems && isAndroid
                    ? t.profile
                        .items_selected(count: store.selectedItems.length)
                    : title ?? t.photos.title,
                style: textTheme.bodyMedium!.copyWith(
                  fontWeight: FontWeight.w700,
                  fontSize: 17,
                ),
              ),
              actions: [
                if (isProfile)
                  Observer(builder: (context) {
                    return store.isHasSelectedItems && isAndroid
                        ? IconButton(
                            onPressed: () {
                              store.markAllSelected();
                            },
                            icon: const Icon(Icons.list),
                          )
                        : TextButton(
                            onPressed: () {
                              store.toggleSelect();
                            },
                            child: Text(
                              store.isSelect && !isAndroid
                                  ? t.common.cancel
                                  : t.common.select,
                              style: TextStyle(color: Colors.white),
                            ));
                  })
              ],
            ),
            bottomNavigationBar: isProfile
                ? BottomBarPhotosFuncs(
                    isPacks: true,
                  )
                : null,
            body: SingleChildScrollView(
              child: Padding(
                padding: EdgeInsets.symmetric(horizontal: 15.w, vertical: 15.h),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (!isProfile)
                      AutoSizeText(
                        t.homeView.ready,
                        minFontSize: 8,
                        style: AppStyles.subTitleTextStyle.copyWith(
                          fontSize: 12.sp,
                        ),
                      ),
                    if (!isProfile)
                      SizedBox(
                        height: 5.h,
                      ),
                    AutoSizeText(
                      title ?? t.photos.photos_ready,
                      style: AppStyles.head1TextStyle.copyWith(
                        fontSize: 17.sp,
                      ),
                    ),
                    SizedBox(
                      height: 5.h,
                    ),
                    if (!isProfile)
                      AutoSizeText(
                        t.photos.account,
                        style: AppStyles.subTitleTextStyle.copyWith(
                          fontSize: 12.sp,
                        ),
                      ),
                    SizedBox(
                      height: 8.h,
                    ),
                    GridView.count(
                      physics: const NeverScrollableScrollPhysics(),
                      scrollDirection: Axis.vertical,
                      crossAxisSpacing: 6,
                      mainAxisSpacing: 6,
                      shrinkWrap: true,
                      crossAxisCount: 3,
                      childAspectRatio: (itemWidth / itemHeight),
                      children: models.map((e) {
                        return MediaItem(
                          model: e,
                          isProfile: isProfile,
                        );
                      }).toList(),

                      //   return GestureDetector(
                      //     onTap: () => _showCustomDialog(e.url),
                      //     child: Container(
                      //       decoration: BoxDecoration(
                      //         borderRadius:
                      //             BorderRadius.circular(AppValues.kRadius),
                      //         image: DecorationImage(
                      //             image: CachedNetworkImageProvider(e.url),
                      //             fit: BoxFit.cover),
                      //       ),
                      //       child: Align(
                      //         alignment: Alignment(0.9, -0.9),
                      //         child: Container(
                      //           width: 18.h,
                      //           height: 18.h,
                      //           child: GestureDetector(
                      //             child: SvgPicture.asset(
                      //               AppIcons.downloadGreyCircle,
                      //             ),
                      //           ),
                      //         ),
                      //       ),
                      //     ),
                      //   );
                      // }).toList(),
                    )
                  ],
                ),
              ),
            ),
          );
        });
      },
    );
  }
}
