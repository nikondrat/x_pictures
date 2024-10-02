import 'dart:io';
import 'dart:math';

import 'package:animated_toggle_switch/animated_toggle_switch.dart';
import 'package:flutter/material.dart';
import 'package:flutter_mobx/flutter_mobx.dart';
import 'package:gap/gap.dart';
import 'package:provider/provider.dart';
import 'package:x_pictures/src/data.dart';

class ProfileView extends StatefulWidget {
  final Function() goHome;
  final Function() goGenerate;
  final int selectedIndex;
  const ProfileView(
      {super.key,
      required this.goHome,
      required this.goGenerate,
      required this.selectedIndex});

  @override
  State<ProfileView> createState() => _ProfileViewState();
}

class _ProfileViewState extends State<ProfileView>
    with SingleTickerProviderStateMixin {
  final List<String> tabs = [
    t.profile.pack,
    t.profile.img,
    t.profile.video,
  ];

  // final List<PackModel> packs = [
  //   PackModel(title: 'Pack 1', length: 10, progress: 6, urls: [
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //   ]),
  //   PackModel(title: 'Pack 1', length: 10, urls: [
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //   ]),
  //   PackModel(title: 'Pack 1', length: 10, urls: [
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //   ]),
  //   PackModel(title: 'Pack 1', length: 10, urls: [
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //   ]),
  //   PackModel(title: 'Pack 1', length: 10, urls: [
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //   ]),
  //   PackModel(title: 'Pack 1', length: 10, urls: [
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //   ]),
  //   PackModel(title: 'Pack 1', length: 10, urls: [
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //   ]),
  //   PackModel(title: 'Pack 1', length: 10, urls: [
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //   ]),
  //   PackModel(title: 'Pack 1', length: 10, urls: [
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //     'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
  //   ]),
  // ];

  final List<MediaModel> images = [
    MediaModel(
      type: MediaType.image,
      url:
          'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      createdDate: DateTime(2024, 7, 10),
    ),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
  ];

  final List<MediaModel> videos = [
    MediaModel(
        type: MediaType.video,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.video,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.video,
        createdDate: DateTime(2024, 7, 10),
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
  ];

  late TabController controller;

  @override
  void initState() {
    controller = TabController(length: 3, vsync: this);
    controller.addListener(() {
      setState(() {});
    });
    super.initState();
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final ThemeData themeData = Theme.of(context);
    final TextTheme textTheme = themeData.textTheme;
    final UserStore userStore = context.read<UserStore>();
    final isIOS = Platform.isIOS;

    return MultiProvider(
        providers: [
          Provider(
              create: (context) => JobsStore(
                  restClient: context.read<Dependencies>().restClient)),
        ],
        builder: (context, child) {
          final JobsStore jobsStore = context.read<JobsStore>();
          final MediaBodyStore mediaBodyStore = context.read<MediaBodyStore>();

          return Observer(builder: (context) {
            return Scaffold(
              appBar: mediaBodyStore.isHasSelectedItems && !isIOS
                  ? AppBar(
                      leading: IconButton(
                          onPressed: () {
                            mediaBodyStore.markAllNotSelected();
                          },
                          icon: const Icon(Icons.close)),
                      title: Text(
                        t.profile.items_selected(
                            count: mediaBodyStore.selectedItems.length),
                        style: textTheme.bodyMedium!.copyWith(
                          fontWeight: FontWeight.w700,
                          fontSize: 17,
                        ),
                      ),
                      actions: [
                        IconButton(
                          onPressed: () {
                            mediaBodyStore.markAllSelected();
                          },
                          icon: const Icon(Icons.list),
                        )
                      ],
                    )
                  : null,
              body: AppBody(
                builder: (windowWidth, windowHeight, windowSize) => SafeArea(
                    child: Padding(
                        padding: HorizontalSpacing.centered(windowWidth) +
                            const EdgeInsets.symmetric(
                                vertical: AppValues.kPadding),
                        child: Column(
                          children: [
                            ProfileInfoWidget(
                              name: userStore.username ?? 'No name',
                              email: userStore.email,
                              url: userStore.imageUrl,
                              onTap: () =>
                                  router.goNamed(AppViews.settingsView),
                            ),
                            const Gap(AppValues.kPadding),
                            Row(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                Expanded(
                                  child: AnimatedToggleSwitch<int>.size(
                                    current: min(controller.index, 2),
                                    iconOpacity: 1.0,
                                    animationDuration:
                                        const Duration(milliseconds: 200),
                                    selectedIconScale: 1.0,
                                    style: ToggleStyle(
                                      backgroundColor:
                                          AppColors.kSecondaryAdditionallyColor,
                                      indicatorColor: AppColors.kPrimaryColor,
                                      borderRadius: BorderRadius.circular(10.0),
                                    ),
                                    values: const [0, 1, 2],
                                    height: 40,
                                    indicatorSize: const Size.fromWidth(200),
                                    iconAnimationType: AnimationType.onHover,
                                    styleAnimationType:
                                        AnimationType.onSelected,
                                    customIconBuilder:
                                        (context, local, global) {
                                      final text = tabs[local.index];
                                      return Center(
                                          child: Text(text,
                                              style: const TextStyle(
                                                  color: AppColors
                                                      .kSecondaryColor)));
                                    },
                                    borderWidth: 0,
                                    onChanged: (i) {
                                      if (mediaBodyStore.isSelect) {
                                        mediaBodyStore.toggleSelect();
                                      }
                                      controller.animateTo(i);
                                    },
                                  ),
                                )
                              ],
                            ),
                            // ToggleSwitch(
                            //   minWidth: 400,
                            //   totalSwitches: 3,
                            //   animate: true,
                            //   animationDuration: 400,
                            //   inactiveBgColor:
                            //       AppColors.kSecondaryAdditionallyColor,
                            //   radiusStyle: true,
                            //   labels: tabs,
                            //   dividerColor:
                            //       AppColors.kSecondaryAdditionallyColor,
                            //   onToggle: (index) {
                            //     if (mediaBodyStore.isSelect) {
                            //       mediaBodyStore.toggleSelect();
                            //     }
                            //     controller.animateTo(index!);
                            //   },
                            // ),
                            Expanded(
                                child: ProfileBody(
                                    jobsStore: jobsStore,
                                    controller: controller,
                                    goHome: widget.goHome,
                                    goGenerate: widget.goGenerate)),
                          ],
                        ))),
              ),
            );
          });
        });
  }
}
