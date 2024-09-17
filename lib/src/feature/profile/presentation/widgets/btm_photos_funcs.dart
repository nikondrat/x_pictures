import 'dart:io';
import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:share_plus/share_plus.dart';
import 'package:svg_flutter/svg_flutter.dart';
import 'package:x_pictures/src/data.dart';

class _Item {
  final Widget icon;
  final String title;
  final Function()? onTap;

  _Item({
    required this.icon,
    required this.title,
    this.onTap,
  });
}

class BottomBarPhotosFuncs extends StatelessWidget {
  final bool isPacks;
  const BottomBarPhotosFuncs({
    super.key,
    this.isPacks = false,
  });

  @override
  Widget build(BuildContext context) {
    final MediaBodyStore store = context.read();
    final isIOS = Platform.isIOS;
    // final isIOS = true;

    return Observer(builder: (context) {
      return
          // ((isPacks && !store.isHasSelectedItems) ||
          (store.isSelect)
              ? BottomBarDecoration(
                  child: Padding(
                    padding: const EdgeInsets.symmetric(
                        vertical: AppValues.kPadding / 2),
                    child: Row(
                      mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                      children: [
                        _Item(
                            icon: Icon(
                              Icons.ios_share,
                              size: 20.h,
                            ),
                            onTap: () {
                              final List<XFile> selectedItems =
                                  store.selectedItems.map((e) {
                                return XFile(e.url);
                              }).toList();
                              Share.shareXFiles(selectedItems);
                            },
                            title: t.profile.send),
                        if (isIOS)
                          _Item(
                              icon: Observer(builder: (context) {
                                return AutoSizeText(t.profile.photos_selected(
                                    count: store.selectedItemsCount));
                              }),
                              title: ''),
                        _Item(
                            icon: SvgPicture.asset(
                              Assets.icons.trashBinMinimalistic,
                              color: Colors.white,
                              height: 20.h,
                              width: 20.h,
                            ),
                            title: t.settings.delete.title),
                      ].map((e) {
                        return GestureDetector(
                          child: Column(
                            mainAxisSize: MainAxisSize.min,
                            children: [
                              e.icon,
                              if (!isIOS) Gap(2.r),
                              if (!isIOS)
                                AutoSizeText(e.title,
                                    style: Theme.of(context)
                                        .textTheme
                                        .titleSmall!
                                        .copyWith(fontSize: 6.sp)),
                            ],
                          ),
                        );
                      }).toList(),
                    ),
                  ),
                )
              : SizedBox.shrink();
    });
    // return BottomNavigationBar(
    //     backgroundColor: AppColors.kAdditionalColor,
    //     items: [
    //       BottomNavigationBarItem(
    //           icon: SvgPicture.asset(Assets.icons.share), label: 'send'),
    //       BottomNavigationBarItem(
    //           icon: SvgPicture.asset(Assets.icons.trashBinMinimalistic),
    //           label: 'delete')
    //     ]);
  }
}
