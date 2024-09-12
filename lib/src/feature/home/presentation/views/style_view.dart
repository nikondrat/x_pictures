import 'dart:io';

import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class StyleView extends StatelessWidget {
  final PacksStore? store;
  const StyleView({super.key, required this.store});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;
    final bool isAndroid = Platform.isAndroid;

    final PacksStore store = this.store ?? context.watch<PacksStore>();

    return Scaffold(
      appBar: isAndroid
          ? AppBar(
              leading: const CustomBackButton(),
              title: Text(
                store.selected.title,
                style: textTheme.bodyMedium!.copyWith(
                  fontWeight: FontWeight.w700,
                ),
              ))
          : null,
      body: AppBody(
        builder: (windowWidth, _, __) => SafeArea(
          top: isAndroid ? true : false,
          child: Stack(
            fit: StackFit.expand,
            children: [
              CustomScrollView(
                slivers: [
                  SliverAppBar(
                    pinned: true,
                    expandedHeight: 400,
                    backgroundColor: colorScheme.surface,
                    leading: isAndroid
                        ? const SizedBox.shrink()
                        : const CustomBackButton(),
                    flexibleSpace: FlexibleSpaceBar(
                        background: StyleBottomWidget(model: store.selected)),
                    bottom: PreferredSize(
                      preferredSize: Size.zero,
                      child: SizedBox(
                        width: double.infinity,
                        child: DecoratedBox(
                          decoration: BoxDecoration(
                            color: colorScheme.surface,
                            borderRadius: const BorderRadius.vertical(
                              top: Radius.circular(AppValues.kRadius * 2),
                            ),
                          ),
                          child: const Text(''),
                        ),
                      ),
                    ),
                  ),
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: HorizontalSpacing.centered(windowWidth),
                      child: StyleViewBody(
                        model: store.selected,
                      ),
                    ),
                  )
                ],
              ),
              Align(
                alignment: Alignment.bottomCenter,
                child: Padding(
                  padding: HorizontalSpacing.centered(windowWidth) +
                      const EdgeInsets.only(bottom: AppValues.kPadding * 2),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.end,
                    children: [
                      GradientButton(
                          onPressed: () {
                            // if (model.onTap != null) {
                            //   model.onTap!(model);
                            // } else {
                            router.pushNamed(AppViews.disclaimarPageRoute,
                                extra: {'store': store});
                            // }
                          },
                          text:
                              //  model.actionTitle ??
                              t.homeView.get_pack),
                    ],
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
