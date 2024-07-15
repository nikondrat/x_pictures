import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class PackView extends StatelessWidget {
  final Function() onBannerTap;
  const PackView({super.key, required this.onBannerTap});

  @override
  Widget build(BuildContext context) {
    return SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Gap(AppValues.kPadding),
          // TODO add packs
          // Column(
          //     mainAxisSize: MainAxisSize.min,
          //     crossAxisAlignment: CrossAxisAlignment.stretch,
          //     children: packs
          //         .map((e) => PackItem(
          //               pack: e,
          //             ))
          //         .toList()),
        ],
      ),
    );
  }
}
