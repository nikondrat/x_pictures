import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class HomeBody extends StatefulWidget {
  final PacksStore store;
  final double windowWidth;

  const HomeBody({super.key, required this.store, required this.windowWidth});

  @override
  State<HomeBody> createState() => _HomeBodyState();
}

class _HomeBodyState extends State<HomeBody> {
  @override
  void initState() {
    widget.store.fetchPacks();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return LoadingWidget<List<PackModel>>(
        future: widget.store.fetchPacksFuture,
        builder: (v) {
          // final List<PackModel> packs = v;
          final Map<String, List<PackModel>> packs = widget.store.groupedPacks;

          return Padding(
              padding: HorizontalSpacing.centered(widget.windowWidth) +
                  const EdgeInsets.only(bottom: AppValues.kPadding),
              child: Column(
                  children: packs.entries.map((e) {
                return BackgroundSection(
                    title: e.key,
                    packs: e.value,
                    onTap: (model) {
                      router.goNamed(AppViews.officePageRoute, extra: {
                        'model': model,
                      });
                    });
              }).toList()));
        });
  }
}
