import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
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
  final ScrollController _scrollController = ScrollController();

  @override
  void initState() {
    widget.store.fetchPacks();
    widget.userStore.getUserData();
    _scrollController.addListener(_onScroll);
    super.initState();
  }

  void _onScroll() {
    if (_scrollController.position.pixels ==
        _scrollController.position.maxScrollExtent) {
      widget.store.nextPage();
    }
  }

  @override
  Widget build(BuildContext context) {
    return LoadingWidget<List<PackModel>>(
        future: widget.store.fetchPacksFuture,
        builder: (v) {
          // final List<PackModel> packs = v;
          final Map<String, List<PackModel>> packs = widget.store.groupedPacks;

          return CustomScrollView(controller: _scrollController, slivers: [
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
            SliverList.separated(
              itemCount: packs.entries.length + 1,
              itemBuilder: (context, index) {
                if (index == packs.entries.length) {
                  return const Center(
                      child: CircularProgressIndicator.adaptive());
                }

                final entry = packs.entries.elementAt(index);

                return Padding(
                    padding: const EdgeInsets.only(left: AppValues.kPadding),
                    child: BackgroundSection(
                        title: entry.key,
                        packs: entry.value,
                        onTap: (model) {
                          widget.store.setSelectedPack(model);

                          switch (widget.store.selected.subcategory) {
                            case Subcategory.removeBg:
                              context.pushNamed(AppViews.toolsView, extra: {
                                'isRemoveBackground': true,
                              });
                            case Subcategory.removeObjects:
                              context.pushNamed(AppViews.toolsView);
                            case Subcategory.enhance:
                              context.pushNamed(AppViews.enhanceView);
                            default:
                              router
                                  .pushNamed(AppViews.officePageRoute, extra: {
                                'store': widget.store,
                              });
                          }
                        }));
              },
              separatorBuilder: (context, index) {
                if (widget.userStore.profileType == ProfileType.basic &&
                    index == 1) {
                  return Padding(
                    padding: const EdgeInsets.only(
                        top: AppValues.kPadding,
                        left: AppValues.kPadding,
                        right: AppValues.kPadding),
                    child: ProUpgradeBtn(onPressed: () {
                      context.pushNamed(AppViews.planView,
                          extra: {'continueAction': () {}});
                    }),
                  );
                }
                return const SizedBox.shrink();
              },
            ),
            // SliverToBoxAdapter(
            //     child: Padding(
            //         padding: const EdgeInsets.only(left: AppValues.kPadding),
            //         child: Column(
            //             children: packs.entries.map((e) {
            //           return BackgroundSection(
            //               title: e.key,
            //               packs: e.value,
            //               onTap: (model) {
            //                 widget.store.setSelectedPack(model);
            //                 router.pushNamed(AppViews.officePageRoute, extra: {
            //                   'store': widget.store,
            //                 });
            //               });
            //         }).toList())))
          ]);
        });
  }
}
