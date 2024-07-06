import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class StyleView extends StatelessWidget {
  final StyleModel model;
  const StyleView({super.key, required this.model});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final ColorScheme colorScheme = themeData.colorScheme;

    return Scaffold(
      appBar: AppBar(
        title: Text(model.title),
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
                        background: StyleBottomWidget(model: model)),
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
                ],
              ),
              Align(
                alignment: Alignment.bottomCenter,
                child: Padding(
                  padding: HorizontalSpacing.centered(windowWidth) +
                      EdgeInsets.only(bottom: AppValues.kPadding * 2),
                  child: SizedBox(
                      height: 80,
                      child: GradientButton(
                          onPressed: () {}, text: t.homeView.get_pack)),
                ),
              )
            ],
          ),
        ),
      ),
      // floatingActionButton:
      //     GradientButton(onPressed: () {}, text: t.homeView.get_pack),
    );
  }
}
