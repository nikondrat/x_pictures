import 'package:collection/collection.dart';
import 'package:flutter/material.dart';
import 'package:gap/gap.dart';
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

  final List<PackModel> packs = [
    PackModel(title: 'Pack 1', length: 10, progress: 6, urls: [
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
    ]),
    PackModel(title: 'Pack 1', length: 10, urls: [
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
    ]),
    PackModel(title: 'Pack 1', length: 10, urls: [
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
    ]),
    PackModel(title: 'Pack 1', length: 10, urls: [
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
    ]),
    PackModel(title: 'Pack 1', length: 10, urls: [
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
    ]),
    PackModel(title: 'Pack 1', length: 10, urls: [
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
    ]),
    PackModel(title: 'Pack 1', length: 10, urls: [
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
    ]),
    PackModel(title: 'Pack 1', length: 10, urls: [
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
    ]),
    PackModel(title: 'Pack 1', length: 10, urls: [
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
      'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
    ]),
  ];

  final List<MediaModel> images = [
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.image,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
  ];

  final List<MediaModel> videos = [
    MediaModel(
        type: MediaType.video,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.video,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
    MediaModel(
        type: MediaType.video,
        url:
            'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg'),
  ];

  late TabController controller;

  @override
  void initState() {
    controller = TabController(length: 3, vsync: this);
    super.initState();
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: AppBody(
        builder: (windowWidth, windowHeight, windowSize) {
          return SafeArea(
            child: Padding(
                padding: HorizontalSpacing.centered(windowWidth) +
                    const EdgeInsets.symmetric(vertical: AppValues.kPadding),
                child: Column(
                  children: [
                    ProfileInfoWidget(
                      name: 'Kary Filatova',
                      email: 'filyapel@yandex.ru',
                      url:
                          'https://sleeklens.com/wp-content/uploads/2020/07/ultimate-beauty.jpg',
                      onTap: () => router.goNamed(AppViews.settingsView),
                    ),
                    const Gap(AppValues.kPadding),
                    Container(
                        decoration: const BoxDecoration(
                            color: AppColors.kSecondaryAdditionallyColor),
                        child: Row(
                            children: tabs.mapIndexed((index, title) {
                          return Expanded(
                              child: CustomTabWidget(
                                  isSelected: index == controller.index,
                                  title: title,
                                  onTap: () {
                                    setState(() {
                                      controller.animateTo(index);
                                    });
                                  }));
                        }).toList())),
                    Expanded(
                      child: TabBarView(controller: controller, children: [
                        PackView(
                          packs: packs,
                          onBannerTap: widget.goHome,
                        ),
                        MediaView(onBannerTap: widget.goGenerate, urls: images),
                        MediaView(onBannerTap: widget.goGenerate, urls: videos),
                      ]),
                    ),
                  ],
                )),
          );
        },
      ),
    );
  }
}
