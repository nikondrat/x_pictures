import 'dart:io';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:flutter_screenutil/flutter_screenutil.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:svg_flutter/svg_flutter.dart';
import 'package:x_pictures/src/data.dart';

class _Item {
  final Widget icon;
  final String title;

  _Item({required this.icon, required this.title});
}

class BottomBarPhotosFuncs extends StatelessWidget {
  const BottomBarPhotosFuncs({super.key});

  @override
  Widget build(BuildContext context) {
    final MediaBodyStore? store = context.read<MediaBodyStore?>();
    final isIOS = Platform.isIOS;
    // final isIOS = true;

    return Container(
      padding: const EdgeInsets.symmetric(vertical: AppValues.kPadding / 2),
      decoration: const BoxDecoration(
        color: AppColors.kSecondaryAdditionallyColor,
        borderRadius: BorderRadius.vertical(
          top: Radius.circular(AppValues.kRadius),
        ),
      ),
      child: SafeArea(
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceEvenly,
          children: [
            _Item(
                icon: Icon(
                  Icons.ios_share,
                  size: 10.r,
                ),
                title: t.profile.send),
            if (isIOS)
              _Item(
                  icon: Observer(builder: (context) {
                    return AutoSizeText(t.profile
                        .photos_selected(count: store!.selectedItemsCount));
                  }),
                  title: ''),
            _Item(
                icon: SvgPicture.asset(
                  Assets.icons.trashBinMinimalistic,
                  color: Colors.white,
                  height: 10.r,
                  width: 10.r,
                ),
                title: t.settings.delete.title),
          ].map((e) {
            return Column(
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
            );
          }).toList(),
        ),
      ),
    );
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
