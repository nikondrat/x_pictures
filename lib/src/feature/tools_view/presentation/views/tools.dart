import 'package:auto_size_text/auto_size_text.dart';
import 'package:cached_network_image/cached_network_image.dart';
import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class ToolsView extends StatelessWidget {
  final StyleModel model;
  final bool isRemoveBackground;
  const ToolsView(
      {super.key, required this.model, this.isRemoveBackground = true});

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final ColorScheme colorScheme = themeData.colorScheme;

    return Provider(
        create: (context) => ToolsViewStore(),
        builder: (context, child) {
          final ToolsViewStore store = Provider.of<ToolsViewStore>(context);

          return StudyingView(
              url:
                  'https://get.wallhere.com/photo/face-women-model-portrait-long-hair-photography-Person-skin-Violetta-child-girl-beauty-smile-eye-woman-portrait-photography-photo-shoot-brown-hair-facial-expression-close-up-121398.jpg',
              child: Scaffold(
                appBar: AppBar(
                  leading: const CustomBackButton(),
                  title: Row(
                    mainAxisAlignment: MainAxisAlignment.center,
                    children: [
                      IconButton(
                          onPressed: () {}, icon: const Icon(Icons.undo)),
                      IconButton(
                          onPressed: () {}, icon: const Icon(Icons.redo)),
                      const Gap(AppValues.kPadding / 2),
                      IconButton(
                          onPressed: () {}, icon: const Icon(Icons.flip)),
                    ],
                  ),
                  actions: [
                    Padding(
                      padding: const EdgeInsets.all(8.0),
                      child: IconButton(
                          onPressed: () {},
                          icon: const Icon(Icons.file_download_outlined)),
                    )
                  ],
                ),
                body: Center(
                  child: CachedNetworkImage(
                      imageUrl:
                          'https://get.wallhere.com/photo/face-women-model-portrait-long-hair-photography-Person-skin-Violetta-child-girl-beauty-smile-eye-woman-portrait-photography-photo-shoot-brown-hair-facial-expression-close-up-121398.jpg'),
                ),
                bottomNavigationBar: Container(
                  decoration: BoxDecoration(
                      border: const Border(
                          top: BorderSide(color: AppColors.kOutlineColor)),
                      borderRadius: BorderRadius.circular(AppValues.kRadius)),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Observer(builder: (_) {
                        return Padding(
                          padding: const EdgeInsets.symmetric(
                              horizontal: AppValues.kPadding),
                          child: Row(
                            children: [
                              AutoSizeText(
                                t.toolsView.size,
                                style: textTheme.bodyLarge,
                              ),
                              Expanded(
                                child: Slider(
                                  value: store.size,
                                  min: 1,
                                  max: 50,
                                  onChanged: store.setSize,
                                  inactiveColor: AppColors.kInactiveColor,
                                ),
                              ),
                              AutoSizeText(
                                '${store.size.toInt()}',
                                style: textTheme.bodyLarge,
                              ),
                            ],
                          ),
                        );
                      }),
                      const Divider(),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceAround,
                        children: [
                          ToolModel(
                              title: t.toolsView.erase,
                              icon: Icons.mode_edit_rounded,
                              onTap: () {}),
                          ToolModel(
                              title: t.toolsView.restore,
                              icon: Icons.auto_fix_high,
                              onTap: () {}),
                          ToolModel(
                              title: isRemoveBackground
                                  ? t.toolsView.background
                                  : t.common.remove,
                              icon: Icons.layers_outlined,
                              onTap: () {
                                if (isRemoveBackground) {
                                  router.goNamed(AppViews.backgroundsView,
                                      extra: {'model': model});
                                } else {
                                  // TODO add func to remove objects
                                }
                              }),
                        ].mapIndexed((i, e) {
                          if (!isRemoveBackground && i == 2) {
                            return Padding(
                              padding: const EdgeInsets.only(
                                  right: AppValues.kPadding * 2,
                                  bottom: AppValues.kPadding / 2),
                              child: GradientButton(
                                onPressed: e.onTap,
                                text: e.title,
                                textStyle: textTheme.bodyLarge,
                                padding: const EdgeInsets.symmetric(
                                    vertical: AppValues.kPadding / 2,
                                    horizontal: AppValues.kPadding),
                              ),
                            );
                          }
                          return Observer(builder: (context) {
                            return Expanded(
                              child: GestureDetector(
                                onTap: () {
                                  store.setSelectedTool(i);

                                  e.onTap();
                                },
                                child: Column(
                                  children: [
                                    Icon(
                                      e.icon,
                                      color: i == store.selectedTool
                                          ? colorScheme.primary
                                          : AppColors.kOutlineColor,
                                      size: 30,
                                    ),
                                    AutoSizeText(
                                      e.title,
                                      style: textTheme.bodyLarge!.copyWith(
                                          color: i == store.selectedTool
                                              ? colorScheme.primary
                                              : AppColors.kOutlineColor),
                                    ),
                                  ],
                                ),
                              ),
                            );
                          });
                        }).toList(),
                      )
                    ],
                  ),
                ),
              ));
        });
  }
}
