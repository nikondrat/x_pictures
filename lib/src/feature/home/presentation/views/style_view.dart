import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class StyleView extends StatelessWidget {
  final PacksStore store;
  const StyleView({super.key, required this.store});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Scaffold(
      appBar: AppBar(
        leading: const CustomBackButton(),
        title: Text(
          store.selected!.title,
          style: textTheme.headlineSmall!.copyWith(fontWeight: FontWeight.w700),
        ),
      ),
      body: AppBody(
        builder: (windowWidth, _, __) => SafeArea(
          child: Stack(
            fit: StackFit.expand,
            children: [
              CustomScrollView(
                slivers: [
                  SliverAppBar(
                    pinned: true,
                    expandedHeight: 400,
                    backgroundColor: colorScheme.surface,
                    leading: const SizedBox(),
                    flexibleSpace: FlexibleSpaceBar(
                        background: StyleBottomWidget(model: store.selected!)),
                    bottom: PreferredSize(
                      preferredSize: Size.zero,
                      child: Container(
                        width: double.infinity,
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
                  SliverToBoxAdapter(
                    child: Padding(
                      padding: HorizontalSpacing.centered(windowWidth),
                      child: StyleViewBody(
                        model: store.selected!,
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
                  child: SizedBox(
                      height: 80,
                      child: GradientButton(
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
                              t.homeView.get_pack)),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
