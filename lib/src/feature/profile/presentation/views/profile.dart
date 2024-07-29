import 'package:collection/collection.dart';
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
    super.initState();
  }

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final UserStore userStore = context.read<UserStore>();

    return MultiProvider(
        providers: [
          Provider(
              create: (context) => JobsStore(
                  restClient: context.read<Dependencies>().restClient)),
          Provider(create: (context) => MediaBodyStore()),
        ],
        builder: (context, child) {
          final JobsStore jobsStore = context.read<JobsStore>();
          final MediaBodyStore mediaBodyStore = context.read<MediaBodyStore>();

          return Observer(builder: (context) {
            return Scaffold(
              appBar: mediaBodyStore.isHasSelectedItems
                  ? AppBar(
                      leading: IconButton(
                          onPressed: () {
                            mediaBodyStore.markAllNotSelected();
                          },
                          icon: const Icon(Icons.close)),
                      title: Text(t.profile.items_selected(
                          count: mediaBodyStore.selectedItems.length)),
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
                              name: userStore.username ?? 'Nikita',
                              email: userStore.email,
                              url: userStore.imageUrl ??
                                  'https://catherineasquithgallery.com/uploads/posts/2021-02/1614511031_164-p-na-belom-fone-chelovek-185.jpg',
                              onTap: () =>
                                  router.goNamed(AppViews.settingsView),
                            ),
                            const Gap(AppValues.kPadding),
                            Container(
                                decoration: const BoxDecoration(
                                    borderRadius: BorderRadius.all(
                                        Radius.circular(AppValues.kRadius)),
                                    color:
                                        AppColors.kSecondaryAdditionallyColor),
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
