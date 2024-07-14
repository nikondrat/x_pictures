import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
import 'package:x_pictures/src/data.dart';

class PackView extends StatefulWidget {
  final PacksStore store;
  final Function() onBannerTap;
  const PackView({super.key, required this.store, required this.onBannerTap});

  @override
  State<PackView> createState() => _PackViewState();
}

class _PackViewState extends State<PackView> {
  @override
  void initState() {
    widget.store.fetchPacks();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return LoadingWidget<List<PackModel>>(
      future: widget.store.fetchPacksFuture,
      emptyData: IntrinsicHeight(
        child: GestureDetector(
          onTap: widget.onBannerTap,
          child: Image.asset(
            Assets.images.banner2.path,
            fit: BoxFit.contain,
          ),
        ),
      ),
      builder: (v) {
        final List<PackModel> packs = v;

        return SingleChildScrollView(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Gap(AppValues.kPadding),
              Column(
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
      },
    );
  }
}
