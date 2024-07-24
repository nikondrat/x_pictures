import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class PackView extends StatelessWidget {
  final Function() onBannerTap;
  const PackView({super.key, required this.onBannerTap});

  @override
  Widget build(BuildContext context) {
    final JobsStore jobsStore = context.read<JobsStore>();

    return SingleChildScrollView(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const Gap(AppValues.kPadding),
          // TODO add packs
          Column(
              mainAxisSize: MainAxisSize.min,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: jobsStore.jobs
                  .map((e) => PackItem(
                        pack: e.pack,
                      ))
                  .toList()),
        ],
      ),
    );
  }
}
