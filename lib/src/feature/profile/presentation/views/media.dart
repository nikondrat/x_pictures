import 'dart:io';

import 'package:auto_size_text/auto_size_text.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class MediaView extends StatelessWidget {
  final Function() onBannerTap;

  const MediaView({
    super.key,
    required this.onBannerTap,
  });

  @override
  Widget build(BuildContext context) {
    final MediaBodyStore store = context.read<MediaBodyStore>();
    final isIOS = Platform.isIOS;

    return Column(
      children: [
        const Gap(AppValues.kPadding),
        if (store.items.isNotEmpty)
          Observer(builder: (context) {
            return Row(
                mainAxisAlignment:
                    //  store.isHasSelectedItems
                    // ? MainAxisAlignment.spaceBetween
                    // :
                    MainAxisAlignment.end,
                children: [
                  if (store.isHasSelectedItems && isIOS)
                    FilledButton(
                        style: const ButtonStyle(
                            backgroundColor: WidgetStatePropertyAll(
                                AppColors.kSecondaryAdditionallyColor)),
                        onPressed: () {
                          store.markAllSelected();
                        },
                        child: AutoSizeText(t.common.select_all)),
                  FilledButton(
                      style: const ButtonStyle(
                          backgroundColor: WidgetStatePropertyAll(
                              AppColors.kSecondaryAdditionallyColor)),
                      onPressed: () {
                        store.toggleSelect();
                      },
                      child: AutoSizeText(
                          store.isSelect ? t.common.cancel : t.common.select)),
                ]);
          }),
        store.items.isEmpty
            ? IntrinsicHeight(
                child: GestureDetector(
                  onTap: onBannerTap,
                  child: Image.asset(
                    Assets.images.banner2.path,
                    fit: BoxFit.contain,
                  ),
                ),
              )
            : const Expanded(child: MediaBody())
      ],
    );
  }
}
