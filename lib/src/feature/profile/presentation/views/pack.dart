import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class PackView extends StatelessWidget {
  final List<PackModel> packs;
  final Function() onBannerTap;
  const PackView({super.key, required this.packs, required this.onBannerTap});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (packs.isNotEmpty) const Gap(AppValues.kPadding),
          packs.isEmpty
              ? IntrinsicHeight(
                  child: GestureDetector(
                    onTap: onBannerTap,
                    child: Image.asset(
                      Assets.images.banner2.path,
                      fit: BoxFit.contain,
                    ),
                  ),
                )
              : Column(
                  mainAxisSize: MainAxisSize.min,
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: packs
                      .map((e) => PackItem(
                            pack: e,
                          ))
                      .toList()),
        ],
      ),
    );
  }
}
