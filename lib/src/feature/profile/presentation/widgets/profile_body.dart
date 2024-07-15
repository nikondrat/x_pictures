import 'package:flutter/material.dart';
import 'package:x_pictures/src/data.dart';

class ProfileBody extends StatefulWidget {
  final JobsStore jobsStore;
  final TabController controller;
  final Function() goHome;
  final Function() goGenerate;
  const ProfileBody({
    super.key,
    required this.jobsStore,
    required this.controller,
    required this.goHome,
    required this.goGenerate,
  });

  @override
  State<ProfileBody> createState() => _ProfileBodyState();
}

class _ProfileBodyState extends State<ProfileBody> {
  @override
  void initState() {
    widget.jobsStore.fetchJobs();
    super.initState();
  }

  @override
  Widget build(BuildContext context) {
    return LoadingWidget(
        future: widget.jobsStore.fetchJobsFuture,
        builder: (v) {
          final List<JobModel> jobs = v;

          return TabBarView(controller: widget.controller, children: [
            PackView(
              onBannerTap: widget.goHome,
            ),
            MediaView(onBannerTap: widget.goGenerate),
            MediaView(onBannerTap: widget.goGenerate),
          ]);
        });
  }
}
