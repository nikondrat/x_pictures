import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class HomeBody extends StatefulWidget {
  final PacksStore store;
  final UserStore userStore;

  final double windowWidth;

  const HomeBody(
      {super.key,
      required this.store,
      required this.userStore,
      required this.windowWidth});

  @override
  State<HomeBody> createState() => _HomeBodyState();
}

class _HomeBodyState extends State<HomeBody> {
  @override
  void initState() {
    widget.store.fetchPacks();
    widget.userStore.getUserData();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return LoadingWidget<List<PackModel>>(
        future: widget.store.fetchPacksFuture,
        builder: (v) {
          // final List<PackModel> packs = v;
          final Map<String, List<PackModel>> packs = widget.store.groupedPacks;

          return CustomScrollView(slivers: [
            SliverToBoxAdapter(
              child: AppBarHomeView(
                // model: sections[0].items[1],
                model: packs.values.first.first,
              ),
            ),
            SliverPadding(
                padding: HorizontalSpacing.centered(widget.windowWidth) +
                    const EdgeInsets.only(top: AppValues.kPadding),
                sliver: const SliverToBoxAdapter(
                  child: SearchBarWidget(),
                )),
            SliverToBoxAdapter(
                child: Padding(
                    padding: HorizontalSpacing.centered(widget.windowWidth) +
                        const EdgeInsets.only(bottom: AppValues.kPadding),
                    child: Column(
                        children: packs.entries.map((e) {
                      return BackgroundSection(
                          title: e.key,
                          packs: e.value,
                          onTap: (model) {
                            widget.store.setSelectedPack(model);
                            router.pushNamed(AppViews.officePageRoute, extra: {
                              'store': widget.store,
                            });
                          });
                    }).toList())))
          ]);
        });
  }
}
