# net_configlib.__init__



__version__ = "2.1.2"



from copy import deepcopy
import os
import sys
import yaml

from deepops import deepmerge, deepremoveitems



# --- functions ---



def _raise_exception(e):
    """Simple function to raise the specified exception.  This is used
    for the parameter onerror for os.walk(), which otherwise ignores
    errors and skips over problematic directory entries.
    """

    raise e



# --- classes ---



class NetInventory(dict):
    """Represents a network configuration inventory - devices, VLANs,
    ACLs, etc.  Inventories can be read from directory hierarchies,
    merged and templates applied.
    """


    def __init__(self, dirname=None, debug=False):
        """The constructor initialises the inventory to be empty.

        Optionally, if a directory name is given, read_dir() will be
        called on that directory and then templates_merge_all()
        applied.
        """


        super().__init__()


        # call the 'clear' method to initialise anything extra

        self.clear()


        # if we were given a directory name, read that and merge any
        # templates

        if dirname:
            self.read_dir(dirname, debug)
            self.templates_merge_all(debug)


    def clear(self):
        """Clear the current inventory, ready to read in a new one.
        """

        super().clear()


        # to avoid creating confusing, overlapping item definitions,
        # read from multiple files, we only permit one instance of a
        # particular type of item to be read
        #
        # the read_filepaths dictionary serves two purposes: to
        # record that a particular instance has already been read, and
        # what file it was read from (to help find the source of the
        # clash)
        #
        # it is a simple two-level dictionary mirroring the inventory:
        # the first level is the type of item (e.g. 'vlans', 'devices')
        # and the second is the instance (e.g. 'voice-law',
        # 'dist-sidg')

        self._filepaths = {}


    def read_dir(self, dirname, debug=False):
        """Walk a directory tree, reading all the files contained
        within and add them to the inventory using read_file().

        Files and directories with names that have leading dots will be
        skipped as they're assumed to be either temporary or some sort
        of system file (including '.git').

        Note that read_file() will not automatically apply templates
        (unlike the constructor).
        """

        # walk the directory tree, raising an exception if there are
        # any problems (oddly, os.walk() doesn't do this by default and
        # skips over any errors)

        for dirpath, dirnames, filenames in \
            os.walk(dirname, onerror=_raise_exception):

            # remove any directories whose name begins with a dot so
            # they're not traversed into on subsequent iterations

            for dirname in dirnames:
                if dirname.startswith("."):
                    dirnames.remove(dirname)


            # work through all the files in this directory, in sorted
            # order, and process them

            for this_filename in sorted(filenames):
                # skip files with names beginning with a dot

                if this_filename.startswith("."):
                    continue


                # read this file as YAML and merge it into the
                # inventory

                this_filepath = os.path.join(dirpath, this_filename)

                if debug:
                    print("debug: reading inventory file: %s"
                              % this_filepath,
                          file=sys.stderr)

                self.read_file(this_filepath)


    def read_file(self, this_filepath):
        """Read in a single file and add it to the inventory.

        To avoid creating items that overlap between two files (and
        create confusing composite definitions), an error will be
        raised if there a file defines a item that already exists at
        the second level.

        Note that read_file() will not automatically apply templates
        (unlike the constructor).
        """

        try:
            this_file = yaml.safe_load(open(this_filepath))

        except yaml.parser.ParserError as exception:
            raise ValueError("failed parsing inventory file: %s: %s"
                                 % (this_filepath, exception))


        if not this_file:
            print("warning: skipping empty inventory file: %s"
                      % this_filepath,
                  file=sys.stderr)

            return


        # work through the types of item in this file

        for item_type in this_file:
            # get the dictionary of filepaths for this type,
            # initialising it to empty, if none have been read yet

            type_filepaths = self._filepaths.setdefault(item_type, {})


            # work through instances of this type in this file

            for item_instance in this_file[item_type]:
                # if we've already read an instance of this type with
                # this name already, raise an exception

                if item_instance in type_filepaths:
                    raise KeyError(
                        "duplicate key: [%s][%s] in file: %s "
                        "first read in file: %s"
                            % (repr(item_type), repr(item_instance),
                               this_filepath, type_filepaths[item_instance]))


                # add this filepath as the source of this instance

                type_filepaths[item_instance] = this_filepath


        # all good - merge this file into the main inventory

        deepmerge(self, this_file)


    def templates_merge_all(self, debug=False):
        """Go through the inventory and apply all templates to all
        items that have them, replacing them.
        """

        # the top level of items in the inventory are item types

        for type_name in self:
            # skip the templates themselves

            if type_name.startswith("template-"):
                continue


            # get the dictionary for this type (which contains the
            # instances of it) as we'll be using it a bit

            instances = self[type_name]


            # go through the instances of this type, replacing the
            # instances with a merged copy

            for instance_name in instances:
                instances[instance_name] = self.templates_merge(
                    type_name, instance_name, debug)


    def templates_merge(self, type_name, instance_name, debug=False):
        """This method recursively merges templates into the instance
        specified (given the type name and instance name) from the
        inventory.  The merged instance is returned and not replaced
        in the inventory.

        If there is no "templates" key in the item, the item is
        returned as is.

        If there is a "templates" key in the item, it is read as a
        list of templates to merge in, with entries in the templates
        later in the list taking precedence.  Each of these is merged
        recursively, allowing them to merge templates themselves,
        and exclude items (see next), if configured.

        If there is a "templates-exclude" key, it is taken as a
        structure giving items in the merged set of templates (above)
        to be removed before the final merge into the item (using
        deepremoveitems()).

        Once the merge and exclude stages are complete, the supplied
        item is merged into the merged/excluded template data (with
        entries in the supplied item taking precedence).

        Keyword arguments:

        type_name -- the name of the type of item in the inventory

        instance_name -- the name of the instance of the type of item
        to be merged

        debug -- if set to True, some messages are output, explaining
        the progress of the merge and exclude processes
        """


        # get the item specified from the inventory

        item = self[type_name][instance_name]


        # if the object is not iterable (so we can't check for a
        # 'templates' specification inside it), we just return the
        # object itself to avoid an error if we try to do that

        try:
            iter(item)

        except TypeError:
            if debug:
                print("debug: skipping templates for non-iterable "
                      "instance type: %s name: %s"
                          % (type_name, instance_name),
                      file=sys.stderr)

            return item


        # return the item as is, if no templates are specified

        if "templates" not in item:
            if debug:
                print("debug: no templates to merge for instance "
                          "type: %s name: %s" % (type_name, instance_name),
                      file=sys.stderr)

            return item


        # check templates for this type exist

        template_type_name = "template-" + type_name

        if template_type_name not in self:
            raise KeyError("template type: %s not found, included in "
                               "instance type: %s name: %s"
                                   % (template_type_name, type_name,
                                      instance_name))


        if debug:
            print("debug: merging templates for type: %s "
                      "name: %s" % (type_name, instance_name),
                  file=sys.stderr)


        # do the merge (potentially recursively)

        instance_merged = self._templates_merge(
            template_type_name, item, [instance_name], debug)


        # remove the 'templates' entry from the item

        deepremoveitems(instance_merged, { "templates"})


        if debug:
            print("debug: merging complete for type: %s name: %s"
                      % (type_name, instance_name),
                  file=sys.stderr)


        return instance_merged


    def _templates_merge(self, template_type_name, item, path, debug=False):
        """This method is called by templates_merge() to do the inner
        workings of the merge process, including recursively by itself.
        It does not perform some checks as these are done once by
        templates_merge() and takes slightly different arguments.

        It largely performs the same as function as templates_merge(),
        except that:

        * it takes a 'template type name' instead of a 'type name' -
          this is an optimisation to avoid recalculating it each
          recursive call - this is the type name with 'template-' on
          the beginning; it does not check if this is present in the
          inventory - that is the responsibility of the caller

        * it takes a dictionary of the item to be merged, rather than
          the name of its instance - this can be the root instance or
          a template that is recursively included

        * it has a 'path' attribute that is used for messages and to
          detect loops in recursion

        * it does not check if an item has a 'templates' entry and
          will raise an exception if not - it is the responsibility of
          the caller to do this (this is mainly to avoid recursing when
          it is not required)

        As with temlates_merge(), the merged item is returned, rather
        than merged in place.

        Keyword arguments:

        template_type_name -- the name of the type in the inventory
        for the templates: essentially just "template-<type>"

        item -- an instance or template definition dictionary that is
        merged into, as described

        path -- a list containing the names of the initial instance and
        templates included by it, in order; it is used for two
        purposes: first, to check if a template has already been
        included and avoid loops in the recursion, and second, when
        reporting exceptions and other messages, to help identify the
        location of a problematic template merge

        debug -- if set to True, some messages are output, explaining
        the progress of the merge and exclude processes
        """

        # this dictionary will be used to build up the composite of all
        # the merged templates and then exclude items, before merging
        # the item into it at the end

        templates_merged = {}


        # in case we need to print it, work out the printable version
        # of the path

        path_str = " -> ".join(path)


        # go through the list of sub templates to merge in this item
        #
        # it is the responsibility of the caller to only run this
        # method where there are templates specified, so we don't have
        # to check if this exists first

        for template_name in item["templates"]:
            # check this particular sub template is defined and abort
            # with an error if not

            if template_name not in self[template_type_name]:
                raise KeyError(
                    "template not found for template type: %s name: "
                        "%s included by path: %s"
                            % (template_type_name, template_name, path_str))


            # check if we've included this sub template already, at
            # some point higher in the hierarchy - if we have, we have
            # an include loop
            #
            # we ignore the first item as that's the instance name (the
            # non-template that starts the include) - it would be
            # confusing if this was also the name of a template but it
            # might be

            if template_name in path[1:]:
                raise RecursionError(
                    "template already included template type: %s "
                        "name: %s included by path: %s"
                            % (template_type_name, template_name, path_str))


            # get the dictionary of the sub template we're including

            sub_template = self[template_type_name][template_name]


            # if there are further sub templates included in this sub
            # template, recursively merge them in and replace it
            #
            # if there aren't we just use the sub template as is

            if "templates" in sub_template:
                if debug:
                    print("debug: recursively merging templates for "
                              "template type: %s name: %s"
                                  % (template_type_name, template_name),
                          file=sys.stderr)

                sub_template = self._templates_merge(
                    template_type_name, sub_template,
                    path + [template_name], debug)

                if debug:
                    print("debug: recursive merging complete for "
                              "template type: %s name: %s"
                                  % (template_type_name, template_name),
                          file=sys.stderr)


            # merge a deepcopy() of this sub template into the
            # composite template we're building
            #
            # we have to deepcopy() it to avoid changing parts of
            # the merged structure here and also if we exclude
            # entries later

            deepmerge(templates_merged, deepcopy(sub_template))


        # if we're excluding anything from the imported templates, we
        # now remove these from the merged template we've just built

        if "templates-exclude" in item:
            if debug:
                print("debug: excluding items from merge", file=sys.stderr)

            deepremoveitems(templates_merged, item["templates-exclude"])


        # finally, we merge the item we were called with (either the
        # instance or a recursively merged template) over the top of
        # the merged/excluded templates; this will give precedence to
        # the ones in this item's definition and avoid changing the
        # item itself

        deepmerge(templates_merged, item)


        return templates_merged


    def get_filepaths(self):
        """Return the paths of files which are the source of each item
        in the inventory.

        This is a two-level deep dictionary which matches the first two
        levels of the inventory.  The source if the first level or
        levels below the second are not tracked as clashes are only
        detected at the second level (see read_file()).
        """

        return self._filepaths